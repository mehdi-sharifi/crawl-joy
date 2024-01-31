#! /bin/bash
kubectl create -f namespace.yml
helm install redis redis --namespace crawljoy-ns
helm install postgres postgres --namespace crawljoy-ns
helm install crawler-app crawler-app --namespace crawljoy-ns