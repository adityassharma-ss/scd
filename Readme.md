Logs Migration to OpenSearch
1. Overview
We are migrating logs from an Azure Storage Account to OpenSearch for indexing and visualization.

Key Components:
Log Ingestion: Read logs from Azure Storage.
Parsing & Transformation: Convert logs into a structured format.
Storage & Indexing: Store logs in OpenSearch.
Visualization: Use OpenSearch Dashboards for log analysis.
2. Architecture & Tools
Component	Purpose
Azure Storage	Source of raw logs (JSON, CSV, etc.)
Logstash / Fluent Bit	Reads logs, processes them, and sends to OpenSearch
OpenSearch	Stores and indexes logs
OpenSearch Dashboards	Visualizes logs and queries data
3. Deployment Setup
3.1 Infrastructure
Component	VM Size (Azure)	Notes
OpenSearch	Standard_D4s_v3 (4 vCPU, 16GB RAM)	Stores & queries logs
Logstash/Fluent Bit	Standard_B2s	Ingests logs and forwards to OpenSearch
OpenSearch Dashboards	Standard_B2s	For visualization & analytics
4. Migration Steps
4.1 Deploy OpenSearch
Install OpenSearch on a VM
sh
Copy
Edit
wget https://artifacts.opensearch.org/releases/bundle/opensearch/2.10.0/opensearch-2.10.0-linux-x64.tar.gz
tar -xzf opensearch-2.10.0-linux-x64.tar.gz
cd opensearch-2.10.0
Configure OpenSearch (opensearch.yml)
yaml
Copy
Edit
cluster.name: opensearch-cluster
network.host: 0.0.0.0
discovery.type: single-node
Start OpenSearch
sh
Copy
Edit
./opensearch-tar-install.sh
4.2 Setup Log Ingestion (Fluent Bit or Logstash)
Option 1: Fluent Bit (Lightweight)
Install Fluent Bit
sh
Copy
Edit
curl -fsSL https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh
Configure Fluent Bit (fluent-bit.conf)
ini
Copy
Edit
[INPUT]
    Name azure_blob
    StorageAccount your_storage_account
    Container your_container_name
    Key your_access_key
[OUTPUT]
    Name opensearch
    Host <OpenSearch_IP>
    Port 9200
    Index logs
    Type _doc
Start Fluent Bit
sh
Copy
Edit
fluent-bit -c fluent-bit.conf
Option 2: Logstash (More Features)
Install Logstash
sh
Copy
Edit
sudo apt update && sudo apt install -y logstash
Configure Logstash Pipeline (logstash.conf)
ini
Copy
Edit
input {
  azure_blob_storage {
    storage_account_name => "your_storage_account"
    container_name => "your_container"
    access_key => "your_access_key"
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  opensearch {
    hosts => ["http://<OpenSearch_IP>:9200"]
    index => "logs"
  }
}
Start Logstash
sh
Copy
Edit
sudo systemctl start logstash
4.3 Connect OpenSearch Dashboards
Deploy OpenSearch Dashboards
sh
Copy
Edit
wget https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/2.10.0/opensearch-dashboards-2.10.0-linux-x64.tar.gz
tar -xzf opensearch-dashboards-2.10.0-linux-x64.tar.gz
cd opensearch-dashboards-2.10.0
./opensearch-dashboards
Configure Dashboards (opensearch_dashboards.yml)
yaml
Copy
Edit
server.host: "0.0.0.0"
opensearch.hosts: ["http://<OpenSearch_IP>:9200"]
Access OpenSearch Dashboards
Open browser → http://<OpenSearch_IP>:5601
Create an index pattern for logs (logs-*).
Start analyzing log data.
5. Optimization & Cost Savings
Optimization	Impact
Use Fluent Bit instead of Logstash	Lower CPU & memory usage
Enable log compression in OpenSearch	Reduces storage costs
Store logs in hot/warm/cold tiers	Optimizes long-term storage
Use Index Lifecycle Management (ILM)	Automatically deletes old logs
6. Summary
✅ Logs extracted from Azure Storage
✅ Ingested into OpenSearch via Fluent Bit or Logstash
✅ Visualized in OpenSearch Dashboards
✅ Cost-optimized with storage management
