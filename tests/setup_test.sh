!/bin/sh

ROLE=role-firewalld
KILL=0

docker run --detach --rm --name $ROLE  --privileged --volume `pwd`:/etc/ansible/roles/$ROLE:ro --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro gitlab..net:4567/-docker/-docker-centos7-ansible:latest /usr/lib/systemd/systemd
docker exec $ROLE ansible --version
docker exec $ROLE yum install cronie -y # install pkgs required for crontab to work
docker exec $ROLE ansible-playbook /etc/ansible/roles/$ROLE/tests/test.yml

if [ $KILL -eq 1 ]
then
  docker kill $ROLE
fi

