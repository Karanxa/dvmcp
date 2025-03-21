# Deploying DVMCP to Model Marketplaces

This guide explains how to deploy the Damn Vulnerable Model Context Protocol (DVMCP) to various model marketplaces.

## Prerequisites

- Docker installed
- Account on target marketplace (Smithery, Glama.ai, etc.)
- Basic understanding of model deployment concepts

## Building the Container

```bash
docker build -t dvmcp:latest .
```

## Marketplace-Specific Instructions

### Smithery Deployment

1. Log in to Smithery:
```bash
smithery login
```

2. Package the model:
```bash
smithery package --model-card model-card.yaml
```

3. Deploy to Smithery:
```bash
smithery deploy dvmcp:latest
```

### Glama.ai Deployment

1. Log in to Glama.ai:
```bash
glama login
```

2. Initialize deployment:
```bash
glama init --model-card model-card.yaml
```

3. Deploy the model:
```bash
glama deploy --docker-image dvmcp:latest
```

## Post-Deployment Verification

After deployment, verify the following endpoints are accessible:

1. Model Loading: `POST /api/v1/model/load`
2. Prediction: `POST /api/v1/model/predict`
3. Admin Token: `POST /api/v1/admin/token`
4. Model Metadata: `GET /api/v1/model/metadata`

## Security Considerations

Remember that this is a deliberately vulnerable application. When deploying to marketplaces:

1. Clearly mark it as an educational tool
2. Set appropriate usage warnings
3. Implement marketplace-specific security policies
4. Monitor for abuse

## Support

For deployment issues or questions:
- Email: researcher@example.com
- GitHub Issues: [Project Issues](https://github.com/your-repo/dvmcp/issues)

## Disclaimer

This application contains intentional vulnerabilities for educational purposes. Deploy only in controlled environments with appropriate warnings and usage restrictions. 