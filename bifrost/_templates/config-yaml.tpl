application:
  type: undefined
bifrost:
  version: 0
connection:
  aws_profile: reservoir
  gateway: True
  instance_username: ubuntu
  region: 'eu-west-1'
  ssh_key: ~/.aws/live.pem
deployment:
  base_dir: /srv/mgr
  code_dir: code
  venv: venv
  user: www-data
repository: ''
dvsc: 'git'
roles: {}
