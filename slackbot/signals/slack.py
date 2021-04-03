from beatnik.models.music import Music
from slackbot.decorators import slackevent
from slackbot.models import Install
from urllib import parse

import slack
import os


@slackevent
def link_shared(payload, **kw):
    print(payload)
    install_record = Install.objects.get(team_id=payload['team_id'])
    event = payload['event']
    if install_record.bot_user_id == event['user']:
        return

    music_obj = None
    for link in event['links']:
        url = parse.urlparse(link['url'])
        if(Music.objects.verify_url(url)):
            music_obj = Music.objects.get_or_create(url)
            break

    if not music_obj:
        return

    lines = list(map(lambda link: ":headphones: " + link, filter(None, [
        music_obj.apple_url,
        music_obj.soundcloud_url,
        music_obj.spotify_url,
        music_obj.tidal_url
    ])))

    lines.insert(0, "Here are some other links to this {}:".format(
        music_obj.get_music_type_display()
    ))

    slack.WebClient(token=install_record.access_token).chat_postMessage(
        channel=event['channel'],
        thread_ts=event.get('thread_ts', event['message_ts']),
        text="\n".join(lines)
    )


@slackevent
def app_uninstalled(payload, **kw):
    Install.objects.filter(team_id=payload['team_id']).delete()
