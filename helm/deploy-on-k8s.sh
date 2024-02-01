#! /bin/bash
kubectl create -f namespace.yml
helm install redis redis --namespace crawljoy-ns
helm install postgres postgres --namespace crawljoy-ns
sleep 60
helm install crawler-app crawler-app --namespace crawljoy-ns