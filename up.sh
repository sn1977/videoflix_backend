git add .
git commit -m "$*"
git push
ssh snemeth1977@35.242.235.177 "cd /home/snemeth1977/projects/videoflix_backend/ && git pull"