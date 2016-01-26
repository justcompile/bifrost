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
roles:
  web: {tag-key: my-web-tag}
  worker: {tag-key: my-worker-tag}
