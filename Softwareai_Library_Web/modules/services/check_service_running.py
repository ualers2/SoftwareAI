import docker

def check_service_running(service_name):
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        running_containers = client.containers.list()
        running_containers_final = any(service_name in container.name for container in running_containers)
        print(f"{running_containers_final}")
        return running_containers_final
    except Exception as e:
        print(f"Erro ao verificar status do serviço {service_name}: {e}")
        return False
