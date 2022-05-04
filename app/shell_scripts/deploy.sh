git add -A
read -p 'commit msg:' msg
git commit -m $msg
git push origin master