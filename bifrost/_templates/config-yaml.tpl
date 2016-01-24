connection:
  aws_profile: reservoir
  gateway: user@ipaddress
  instance_username: ubuntu
  regions: [eu-west-1]
  ssh_key: ~/.aws/live.pem
deployment:
  base_dir: /srv/mgr
  code_dir: code
  venv: venv
repository: ''
roles:
  web: {tag-key: my-web-tag}
  worker: {tag-key: my-worker-tag}
