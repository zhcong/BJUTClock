for i in {1..1440}
do
    net_s=`curl -s --head http://10.21.250.3:8080 | sed -n 3p | awk '{print $6}' | awk -F: '{print $3}'`
    local_s=`date | awk '{print $5}' | awk -F: '{print $3}'`
    t=`echo "$net_s-$local_s" | bc`
    echo $t
    echo $t >> s.txt
    sleep 60
done