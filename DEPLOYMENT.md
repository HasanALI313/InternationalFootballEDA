# InternationalFootballEDA - CI/CD Deployment Guide

## Overview
This project uses Declarative Automation Bundles (DABs) for CI/CD deployment across multiple environments.

## Bundle Structure

```
InternationalFootballEDA/
├── databricks.yml           # Main bundle configuration
├── src/
│   ├── Bronze.ipynb        # Data ingestion
│   ├── Silver.ipynb        # Data transformation
│   ├── Gold.ipynb          # Analytics layer
│   ├── Other_dim_data.ipynb
│   ├── Game_Classification_Model.ipynb
│   ├── World Cup 2026 Simulation.ipynb
│   └── utill_funcs.py
└── .gitignore
```

## Environments

### Development (dev)
- **Mode**: development
- **Catalog**: `wc_2026_predions_dev`
- **Purpose**: Testing and development
- **Default**: Yes

### Staging (staging)
- **Mode**: production
- **Catalog**: `wc_2026_predions_staging`
- **Purpose**: Pre-production validation

### Production (prod)
- **Mode**: production
- **Catalog**: `wc_2026_predions`
- **Purpose**: Production workloads

## Jobs Defined

1. **Bronze Layer Ingestion**
   - Runs daily at 2:00 AM UTC
   - Ingests raw football data

2. **Silver Layer Transformation**
   - Runs daily at 2:30 AM UTC
   - Transforms and cleanses data
   - Includes dimension data processing

3. **Gold Layer Analytics**
   - Runs daily at 3:00 AM UTC
   - Creates aggregated analytics tables

4. **ML Model Training**
   - Runs daily at 4:00 AM UTC (PAUSED by default)
   - Trains game classification model

5. **World Cup 2026 Simulation**
   - Runs weekly on Sunday at 5:00 AM UTC (PAUSED by default)
   - Simulates tournament outcomes

## Deployment Commands

### Validate Configuration
```bash
databricks bundle validate --target dev
```

### Deploy to Development
```bash
databricks bundle deploy --target dev
```

### Deploy to Staging
```bash
databricks bundle deploy --target staging
```

### Deploy to Production
```bash
databricks bundle deploy --target prod
```

### Run a Specific Job
```bash
# Dev environment
databricks bundle run bronze_layer_ingestion --target dev

# Production environment
databricks bundle run gold_layer_analytics --target prod
```

### View Bundle Summary
```bash
databricks bundle summary --target dev
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy DAB

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
      
      - name: Validate Bundle
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: databricks bundle validate --target staging
      
      - name: Deploy to Staging
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: databricks bundle deploy --target staging
```

## Configuration Variables

Edit `databricks.yml` to customize:

- **Catalogs**: Change catalog names for each environment
- **Schemas**: Modify bronze/silver/gold schema names
- **Schedules**: Adjust cron expressions for job timing
- **Cluster Configurations**: Update worker counts, node types, Spark versions
- **Email Notifications**: Add/remove notification recipients

## Best Practices

1. **Always validate** before deploying:
   ```bash
   databricks bundle validate --target <env>
   ```

2. **Test in dev** before promoting to staging/prod:
   ```bash
   databricks bundle deploy --target dev
   databricks bundle run <job_name> --target dev
   ```

3. **Use version control**: Commit all changes to Git before deploying

4. **Review changes**: Use `databricks bundle summary` to see what will be deployed

5. **Monitor jobs**: Check job runs in the Databricks workspace after deployment

## Troubleshooting

### Bundle validation fails
- Check YAML syntax
- Ensure all notebook paths exist
- Verify catalog/schema names

### Job fails to run
- Check notebook cell outputs for errors
- Verify cluster configuration
- Check catalog permissions

### Resource conflicts
- Bundle will update existing resources by default
- Resources are tagged with bundle identifiers

## Next Steps

1. Initialize Git repository (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial DAB setup"
   ```

2. Deploy to development:
   ```bash
   databricks bundle deploy --target dev
   ```

3. Test the deployment:
   ```bash
   databricks bundle run bronze_layer_ingestion --target dev
   ```

4. Set up CI/CD pipeline in your Git provider

## Support

For issues or questions about Declarative Automation Bundles, see:
- [Databricks DAB Documentation](https://docs.databricks.com/dev-tools/bundles/)
