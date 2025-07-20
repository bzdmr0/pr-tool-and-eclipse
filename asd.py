from github import Github
import os
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText

#asdasdaasdasd1111222233333

# Initialize GitHub client with your personal access token from environment variable
# Set your token with: export GITHUB_TOKEN="your_token_here"
token = os.getenv('GITHUB_TOKEN') or "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"
if not token:
    print("Error: Please set your GitHub token as an environment variable:")
    print("export GITHUB_TOKEN='your_token_here'")
    exit(1)

g = Github(token)

def get_current_git_branch():
    """Get the current Git branch name"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def bulk_commit_changes(auto_push=True):
    """Create a commit with multiple file changes"""
    try:
        # Get all modified files
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("No changes to commit")
            return False
        
        print("Modified files:")
        print(result.stdout)
        
        commit_message = input("Enter commit message: ").strip()
        if not commit_message:
            commit_message = f"Auto commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Create commit
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        
        print(f"Bulk commit created: {commit_message}")
        
        # Auto-push to GitHub if enabled
        if auto_push:
            try:
                current_branch = get_current_git_branch()
                subprocess.run(['git', 'pull', 'origin', current_branch], check=True)
                subprocess.run(['git', 'push', 'origin', current_branch], check=True)
                print("Successfully pushed to GitHub!")
            except subprocess.CalledProcessError as push_error:
                print(f"Commit created locally but failed to push: {push_error}")
                print("Run 'git push' manually to sync with GitHub")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating bulk commit: {e}")
        return False

def create_pull_request():
    try:
        # Get repository details from user
        repo_name = "bzdmr0/pr-tool-and-eclipse"
        
        # Get the repository
        repo = g.get_repo(repo_name)
        
        # Get pull request details from user
        title = input("Enter pull request title: ").strip()
        if not title:
            title = "New Pull Request"
            
        body = input("Enter pull request description: ").strip()
        if not body:
            body = "Description of changes"
            
        # Get current Git branch automatically
        head_branch = get_current_git_branch()
        if not head_branch:
            print("Could not detect current Git branch")
            head_branch = input("Enter source branch (branch to merge FROM): ").strip()
            
        base_branch = input("Enter target branch (branch to merge TO): ").strip()
        if not base_branch:
            base_branch = "main"
            print(f"Using default target branch: {base_branch}")

        ##asdasdas
        
        # Create a pull request
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,  # The branch you want to merge FROM
            base=base_branch   # The branch you want to merge TO
        )
        
        print(f"Pull request created successfully!")
        print(f"PR URL: {pr.html_url}")
        print(f"PR Number: {pr.number}")
        
        return pr
        
    except Exception as e:
        print(f"Error creating pull request: {e}")
        return None
    
def compile_by_eclipse():
    # CONFIGURATION: Set these for your email
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_FROM = 'bzdmrsaid@gmail.com'
    EMAIL_TO = 'snapchaticin932@gmail.com'
    EMAIL_SUBJECT = '[ALERT] Compilation Failed'
    EMAIL_USER = 'bzdmrsaid@gmail.com'
    EMAIL_PASS = 'iwgo cdbu hrmn yonh '  # Use an App Password if 2FA is enabled

    # Paths (edit as needed)
    source_file = "/home/bzdmr/eclipse-workspace/newProject1/test.c"  # Updated path
    output_dir = "/home/bzdmr/eclipse-workspace/newProject1/Debug"
    output_binary = os.path.join(output_dir, "test")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Compilation command
    compile_cmd = ["gcc", source_file, "-o", output_binary]

    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
        print("Compilation succeeded.")
    except subprocess.CalledProcessError as e:
        print("Compilation failed!")
        # Prepare the email
        body = f"Compilation of {source_file} failed.\n\nError Output:\n{e.stderr}"
        msg = MIMEText(body)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        # Send the email
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
            print("Error email sent.")
        except Exception as mail_err:
            print("Failed to send email:", mail_err)

if __name__ == "__main__":
    print("GitHub PR & Commit Manager")
    print("=" * 40)

    #push_choice = input("Auto-push to GitHub? (y/n, default: y): ").strip().lower()
    #auto_push = push_choice != 'n'
    #bulk_commit_changes(auto_push)

    create_pull_request()
    
    compile_by_eclipse()



# Note: The above code assumes you have the `PyGithub` library installed.

