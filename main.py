# Azure Redis Cache Documentation

## Overview

This document provides details about the Azure Redis Cache tiers (Basic, Standard, Premium), including differences in features, networking, pricing, and security recommendations. It also includes a Terraform script to provision these caches in Azure.

---

## Table of Contents

- [Azure Redis Cache Versions](#azure-redis-cache-versions)
  - [Features Comparison](#features-comparison)
  - [Networking](#networking)
  - [Pricing](#pricing)
  - [New Features](#new-features)
- [Test Cases for Azure Redis Cache](#test-cases-for-azure-redis-cache)
- [Security Recommendations](#security-recommendations)
- [Terraform Scripts for Redis Cache](#terraform-scripts-for-redis-cache)

---

## Azure Redis Cache Versions

Azure Redis Cache comes in three tiers: **Basic**, **Standard**, and **Premium**. Below is a comparison of their features, networking capabilities, pricing, and new features available in each tier.

### Features Comparison

| **Feature**                | **Basic**                  | **Standard**                  | **Premium**                            |
| -------------------------- | -------------------------- | ----------------------------- | -------------------------------------- |
| **Cache Size**              | Up to 53 GB                 | Up to 53 GB                   | Up to 1.2 TB                           |
| **High Availability**       | No                          | Yes (with replication)        | Yes (with persistence, clustering)     |
| **Scaling**                 | No scaling support          | Manual scaling available      | Scaling with Redis clustering          |
| **Persistence**             | No data persistence         | No data persistence           | Data persistence available             |
| **Redis Clustering**        | Not available               | Not available                 | Available                              |
| **VNet Support**            | No                          | No                            | Yes                                    |
| **Redis Modules**           | Not available               | Not available                 | Available (e.g., RediSearch, RedisBloom)|
| **Geo-Replication**         | Not available               | Not available                 | Available                              |

### Networking

- **Basic and Standard** tiers cannot be deployed in a Virtual Network (VNet).
- **Premium** tier can be deployed in a Virtual Network, ensuring isolated network access and increased security through Azure Private Link.

### Pricing

| **Tier**     | **Approx. Monthly Cost** |
| ------------ | ------------------------ |
| **Basic**    | Low (for dev/test)        |
| **Standard** | Medium                    |
| **Premium**  | High (for production)     |

### New Features

- **Premium** tier supports Redis Modules, including RediSearch, RedisBloom, and TimeSeries.
- **Geo-Replication** is available only in the **Premium** tier.
- **Clustering** and **data persistence** are also exclusive to the **Premium** tier.

---

## Test Cases for Azure Redis Cache

Here are some key test cases for validating the functionality of an Azure Redis Cache instance:

1. **Connectivity Test:**
   - Ensure that the Redis Cache instance can be reached from within your application environment.
   
2. **Authentication Test:**
   - Verify that access keys or Azure Active Directory (AAD) authentication is required to connect to the cache.
   
3. **Data Persistence Test (Premium Only):**
   - Validate that the Redis Cache can persist data across resets, if persistence is enabled.
   
4. **Backup and Restore:**
   - Test the backup and restore functionality for Premium Redis instances.
   
5. **Cache Hit/Miss Ratio:**
   - Measure the cache hit/miss ratio to evaluate performance efficiency.

6. **Scaling Test (Standard and Premium):**
   - Test the behavior of the Redis instance when scaling vertically (Standard) or horizontally (Premium).

---

## Security Recommendations

To ensure the security of your Azure Redis Cache instances, follow these recommendations:

- **SSL Encryption:** Enable SSL/TLS for all communications between clients and Redis Cache.
- **Virtual Network (VNet):** Deploy Redis inside a VNet for network isolation (Premium only).
- **Redis Access Keys:** Regularly rotate access keys and use only secure, managed identities when possible.
- **Private Link:** Use Azure Private Link to connect to Redis Cache without exposing it to the public internet.
- **Firewall Rules:** Configure IP firewall rules to limit access to Redis Cache from trusted IP ranges only.

---

## Terraform Scripts for Redis Cache

Below are Terraform scripts to deploy Redis Cache instances in Basic, Standard, and Premium tiers:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

# Basic Tier Redis Cache
resource "azurerm_redis_cache" "example_basic" {
  name                = "example-basic-cache"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku_name            = "Basic"
  capacity            = 1
  enable_non_ssl_port = false
}

# Standard Tier Redis Cache
resource "azurerm_redis_cache" "example_standard" {
  name                = "example-standard-cache"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku_name            = "Standard"
  capacity            = 2
  enable_non_ssl_port = false
}

# Premium Tier Redis Cache
resource "azurerm_redis_cache" "example_premium" {
  name                = "example-premium-cache"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku_name            = "Premium"
  capacity            = 4
  shard_count         = 2
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  redis_configuration {
    maxmemory_policy = "allkeys-lru"
  }
}
