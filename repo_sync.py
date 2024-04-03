import subprocess
from typing_extensions import Annotated
import typer
import github

def get_installation_access_token(app_id: int, private_key: str,
                                  installation_id: int) -> str:
    """
    Obtain an installation access token using JWT.

    Args:
    - app_id (int): The application ID for GitHub App.
    - private_key (str): The private key associated with the GitHub App.
    - installation_id (int): The installation ID of the GitHub App for a particular account.

    Returns
    - Optional[str]: The installation access token. Returns `None` if there's an error obtaining the token.

    """
    integration = github.GithubIntegration(app_id, private_key)
    auth = integration.get_access_token(installation_id)
    assert auth
    return auth.token

# TODO: this may not be required
# def create_mongodb_bot_gitconfig():
#     """Create the mongodb-bot.gitconfig file with the desired content."""

#     content = """
#     [user]
#         name = MongoDB Bot
#         email = mongo-bot@mongodb.com
#     """

#     gitconfig_path = os.path.expanduser("~/mongodb-bot.gitconfig")

#     with open(gitconfig_path, 'w') as file:
#         file.write(content)

#     print("mongodb-bot.gitconfig file created.")


def main(branch: Annotated[str, typer.Option(envvar="GITHUB_REF")],
         app_id: Annotated[int, typer.Option(envvar="APP_ID")],
         installation_id: Annotated[int, typer.Option(envvar="INSTALLATION_ID")],
         server_docs_private_key: Annotated[str, typer.Option(envvar="SERVER_DOCS_PRIVATE_KEY")]):

    access_token = get_installation_access_token(app_id, server_docs_private_key, installation_id)

    # Create the mongodb-bot.gitconfig file as necessary.
    # TODO: this may not be required
    # create_mongodb_bot_gitconfig()

    git_destination_url_with_token = f"https://x-access-token:{access_token}@github.com/mongodb/docs.git"

    # Use a local path for testing
    # git_destination_url_with_token = "path_to_local_git"

    # Add the destination repo and name it upstream
    subprocess.run(["git", "remote", "add", "upstream", git_destination_url_with_token], check=True)
    # Push the code upstream
    subprocess.run(["git", "push", "upstream", branch], check=True)


if __name__ == "__main__":
    typer.run(main)