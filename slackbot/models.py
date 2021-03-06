from django.db.models import Index, Model, TextField


class Install(Model):
    app_id = TextField("Install-specific app ID")
    authed_user_id = TextField("Installing user ID")
    scope = TextField("OAuth scopes granted")
    access_token = TextField("OAuth access token")
    bot_user_id = TextField("Install-specific bot ID")
    team_name = TextField("Workspace name")
    team_id = TextField("Workspace ID", unique=True)

    class Meta:
        indexes = [
            Index(fields=['team_id']),
        ]
