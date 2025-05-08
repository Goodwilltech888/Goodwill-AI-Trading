aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker build -t bitget_trader -f bitget_trader/Dockerfile .
docker tag bitget_trader:latest YOUR_ECR_REPO_URL:latest
docker push YOUR_ECR_REPO_URL:latest