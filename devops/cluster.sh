#!/usr/bin/expect
set podname [lindex $argv 0]
set ids [lrange  $argv 1 6]
set timeout 120

spawn kubectl exec -it -n fire-hydrant $podname bash


expect "*#" {
    send "redis-cli --cluster create $ids --cluster-replicas 1\r"
}
expect "*yes*" {
    send "yes\r"
}

expect "*#" {
    send "exit\r"
}