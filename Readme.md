# **Fetching Metrics from Azure Monitor to Grafana**

## **1. Introduction**
Azure Monitor is a built-in monitoring service that collects metrics and logs from various Azure resources. Grafana can be integrated with Azure Monitor to fetch these metrics directly, eliminating the need for additional exporters or intermediate storage systems like Prometheus.

This document provides a step-by-step guide to integrating Azure Monitor with Grafana for real-time metric visualization.

---

## **2. Prerequisites**
Before proceeding, ensure you have the following:

- **Azure Subscription** with Azure Monitor enabled.
- **Grafana Installed** (either on-premises or via Azure Grafana service).
- **Azure Service Principal** with `Monitoring Reader` permissions.

---

## **3. Creating a Service Principal for Authentication**
To allow Grafana to access Azure Monitor, we need to create a Service Principal with the correct permissions.

### **Step 1: Create a Service Principal**
Run the following command in **Azure CLI**:
```sh
az ad sp create-for-rbac --name "grafana-sp" --role "Monitoring Reader" --scopes /subscriptions/<SUBSCRIPTION_ID>
```
This command will output credentials in JSON format:
```json
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "password": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
  "tenant": "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
}
```
- `appId` → Client ID
- `password` → Client Secret
- `tenant` → Tenant ID

Save these credentials securely, as they will be required to configure Grafana.

### **Step 2: Assign Monitoring Reader Role**
Assign the **Monitoring Reader** role to this Service Principal:
```sh
az role assignment create --assignee <appId> --role "Monitoring Reader" --scope /subscriptions/<SUBSCRIPTION_ID>
```

---

## **4. Configuring Azure Monitor in Grafana**

### **Step 1: Add Azure Monitor as a Data Source**
1. Open **Grafana** and navigate to **Configuration → Data Sources**.
2. Click **“Add data source”** and select **“Azure Monitor”**.
3. Enter the following details:
   - **Subscription ID** → Found in Azure Portal
   - **Tenant ID** → From the Service Principal
   - **Client ID (App ID)** → From the Service Principal
   - **Client Secret** → From the Service Principal
   - **Azure Cloud** → Select `Azure` (or `Azure China` if applicable)

4. Click **"Save & Test"**.
   - If successful, you will see a confirmation message indicating that Grafana can access Azure Monitor.

---

## **5. Visualizing Metrics in Grafana**

### **Step 1: Create a New Dashboard**
1. Go to **Dashboards → Create → New Panel**.
2. Select **Azure Monitor** as the data source.
3. Choose the **Resource Type** (e.g., `Virtual Machines`, `App Services`).
4. Select the **Metric Name** (e.g., `CPU Usage`, `Memory Percentage`).
5. Apply filters (if needed) and set the visualization type (e.g., line graph, bar chart).
6. Click **Save Dashboard**.

---

## **6. Querying Logs from Azure Monitor (Optional)**
Grafana can also fetch logs from Azure Log Analytics using the **Azure Monitor Logs** data source.

### **Step 1: Enable Log Analytics Workspace**
1. In **Azure Portal**, go to **Azure Monitor → Logs**.
2. Create a new **Log Analytics Workspace** (if not already available).

### **Step 2: Configure Grafana for Log Queries**
1. In **Grafana**, go to **Configuration → Data Sources**.
2. Select **Azure Monitor** and enable **Azure Monitor Logs**.
3. Add the **Workspace ID** from Azure Log Analytics.
4. Use **Kusto Query Language (KQL)** to query logs.
   Example Query:
   ```kql
   AzureDiagnostics
   | where TimeGenerated > ago(24h)
   | project TimeGenerated, Resource, Category, Message
   ```
5. Save and visualize the logs.

---

## **7. Benefits of Direct Integration**

| Feature | Benefit |
|---------|---------|
| No need for Prometheus | Saves infrastructure costs |
| Direct real-time monitoring | Reduces data lag |
| Less setup effort | No custom exporters needed |
| Supports logs as well | Unified observability |
| Secure authentication | Uses Azure RBAC |

---

## **8. Optimization & Cost Considerations**
- **Reduce API calls** by increasing Grafana’s refresh interval.
- **Use dashboards efficiently** to avoid unnecessary data queries.
- **Monitor API rate limits** to prevent excessive Azure costs.
- **Enable caching** where possible to improve performance.

---

## **9. Conclusion**
✅ **Metrics fetched from Azure Monitor into Grafana**
✅ **No need for Prometheus or additional exporters**
✅ **Live monitoring with customizable dashboards**

This setup provides a **cost-effective, scalable, and real-time monitoring solution** by leveraging **Azure Monitor’s native integration with Grafana**.

Would you like to automate this setup using Terraform or Ansible? 🚀

