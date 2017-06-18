from flask import (
    Flask,
    request,
    render_template,
    flash,
)
import paramiko
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjvasvayqu13w1rggrdw'


@app.route('/', methods=['GET', 'POST'])
def index():
    users = list()
    with_interactive_shell = list()
    with_root_access = list()
    if request.method == 'POST':
        remote_ip = request.form.get('ip').strip()
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # SSH into remote system using the credentials provided
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=remote_ip, username=username, password=password)
        except socket.error, err:
            flash(str(err), category='error')
            return render_template('index.html')

        # Step 1: Parse /etc/passwd file for getting all users and
        # check whether they have interactive shell access
        stdin, stdout, stderr = ssh.exec_command('sudo cat /etc/passwd')
        content = stdout.readlines()
        for line in content:
            user = line.split(":")[0]
            users.append(user)
            if line.rstrip("\n").split(":")[6] not in ["/usr/sbin/nologin", "/bin/false"]:
                with_interactive_shell.append(user)

        # Step 2: Parse /etc/group file for getting to know all root users
        stdin, stdout, stderr = ssh.exec_command('sudo cat /etc/group')
        content = stdout.readlines()
        for line in content:
            if line.rstrip("\n").__contains__("sudo"):
                with_root_access.append(line.rstrip("\n").split(":")[3])

        ssh.close()
    return render_template(
        'index.html',
        users=users,
        with_root_access=with_root_access,
        with_interactive_shell=with_interactive_shell
    )

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
