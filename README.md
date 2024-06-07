# Development of Cloud Native Apps

This is the repo for the different files and LABs developed for the class "Cloud Native Development" imparted by Javier Cañadillas.

## LAB1: Intro to Kubernetes
We created a K8s cluster with 3 nodes with HA in a region. Here we tested different things like setting up a GKE cluster, creating pods, deployments and services, as well as deployment patterns like blue-green.

### 1. Create K8s cluster:
Created with gcloud command:
```bash
gcloud container clusters create my-cluster --num-nodes=3 --region=europe-west1
```
---

### 2. Creating a Pod:
2.1. First create a repo for my image:
```bash
gcloud artifacts repositories create my-repo --repository-format=docker --location=europe-west1
```

2.2. Push the image to the registry:
```bash
gcloud builds submit -t europe-west1-docker.pkg.dev/$PROJECT_ID/my-repo/hello .
```

Create the pod manifest with:
```bash
envsubst < hello-pod.yaml.template > hello-pod.yaml
```
It substitutes the actual project ID for the variable "PROJECT_ID" in the manifest template.

2.3. Now we're ready to apply:
```bash
kubectl apply -f hello-pod.yaml
```
Access the pod:
```bash
kubectl port-forward hello-pod 8080:8080
```
---

### 3. Containers vs Pods:
In this part we created a pod with 2 containers (1st and 2nd).
This is the summary of the explanation provided by Gemini:
```text
This manifest creates a Pod with two containers. The first container serves the content from the html volume, which is initially empty. The second container continuously updates a file in the html volume with the current date and time. This setup allows you to observe the changes in the file served by the first container.
```
Nice summary

In this exercise we also applied the pod in a different "test" namespace.

Here's a screenshot of the dates (1st) container in action:
![screenshot of mc1 1st output](./img/dates.png)

The 2nd container writes the date in the `html` volume and the 1st reads it and exposes it to the port 8080.

---

### 4. Deployments
After creating the deployment manifest template we have to substitute the PROJECT_ID again:
```bash
envsubst < hello-deployment.yaml.template > hello-deployment.yaml
```
This will create the actual deployment manifest.

Now apply:
```bash
kubectl apply -f hello-deployment.yaml
```

Checking the status of the deployment, we can see the pods we just created with:
```bash
kubectl get pods -l app=hello
```

Output:
```console
NAME                                READY   STATUS    RESTARTS   AGE
hello-deployment-6dd4f6b944-5cl49   1/1     Running   0          42s
hello-deployment-6dd4f6b944-bcvfq   1/1     Running   0          41s
hello-deployment-6dd4f6b944-qnv7w   1/1     Running   0          41s
```
With this we can see that our deployment has the desired number of replicas (3) we asked for.

If I check my pods right after I deleted the first one I have this output:
```console
NAME                                READY   STATUS              RESTARTS   AGE
hello-deployment-6dd4f6b944-bcvfq   1/1     Running             0          2m51s
hello-deployment-6dd4f6b944-cz8f4   0/1     ContainerCreating   0          4s
hello-deployment-6dd4f6b944-qnv7w   1/1     Running             0          2m51s
```
We can see that Kubernetes will automatically create a new pod in order to guarantee the initial manifest. That's why we see the status `ContainerCreating`

After increasing the amount of replicas from 3 to 5 I saw that the deployment kept the previous pods and just added the 2 new ones.

### 5. Services
So far I could only access the pods individually. Let's fix that with a service (load balancer) that exposes all my pods.

After creating the manifest we must again, apply (easy peasy):
```bash
kubectl apply -f hello-service.yaml
```

With the `selector` I'm telling the service to route traffic to my existing deployment.