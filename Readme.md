Ansible-Playbook-Runner is a simple web server for managing and running ansible playbook.
This can be used to deploy builds and releases with a different number of components without creating new playbooks.
You can upload any playbooks and run it in any order.
Server can build a dependency tree (by import_playbook).
Server support ansible vault. You can set vault secret in Run menu.

Used Concept:
Project - main unit in runner. Project contains other artifacts: playbooks, inventories files, Playbook sets and results of running.
Playbook tree - list of all playbooks (yml or yaml files with hosts or import_playbook tag) in project with dependencies. Notice: Del button remove file only for Playbook set (not from disk)
Inventory contains ansible inventory file. Runner support ansible structure like group_vars and host_vars.
Playbook set - list of playbook selected by user for run. One playbook can be repeated several times.
Run used to start selected Playbook set with selected inventory and contains result log

Limitation:
Max depth of tree is 10 (to avoid loops)

Run in container:
1) Build image from Dockerfile
2) Run Container with command:
docker run -p 8000:8000 -v <folder for Project>:/opt/Projects -v <folder for database>/db.sqlite3:/opt/runner/ansible-playbook-runner/db.sqlite3 --name <ContainerName> <ContainerImage>