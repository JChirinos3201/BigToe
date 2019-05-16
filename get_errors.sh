rm errors.txt
scp root@206.81.1.145:/var/log/apache2/error.log errors.txt
python3 format_errors.py
open errors.txt
