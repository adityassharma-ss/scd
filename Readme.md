```
- name: Deploy Node Exporter
  hosts: all
  become: yes
  vars:
    node_exporter_version: "1.5.0"
  tasks:
    - name: Download Node Exporter
      get_url:
        url: "https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/node_exporter-{{ node_exporter_version }}.linux-amd64.tar.gz"
        dest: "/tmp/node_exporter.tar.gz"

    - name: Extract Node Exporter
      unarchive:
        src: "/tmp/node_exporter.tar.gz"
        dest: "/usr/local/bin/"
        remote_src: yes

    - name: Create systemd service for Node Exporter
      copy:
        dest: /etc/systemd/system/node_exporter.service
        content: |
          [Unit]
          Description=Node Exporter
          After=network.target

          [Service]
          User=root
          ExecStart=/usr/local/bin/node_exporter

          [Install]
          WantedBy=default.target
      notify:
        - Reload systemd

    - name: Enable and start Node Exporter
      systemd:
        name: node_exporter
        enabled: yes
        state: started

  handlers:
    - name: Reload systemd
      command: systemctl daemon-reload
```
