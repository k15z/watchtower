.PHONY: deploy fix-lint

deploy:
	npm run build
	aws s3 cp --recursive dist s3://admob-watchtower-public/www
	aws cloudfront create-invalidation --distribution-id E38NGSC2IDES1E --paths "/*"

fix-lint:
	npm run lint
