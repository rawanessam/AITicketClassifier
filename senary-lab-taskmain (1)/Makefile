# Makefile for easy Docker Compose management

.PHONY: help build up down logs clean dev prod

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all services
	docker-compose build

up: ## Start all services in production mode
	docker-compose up -d

dev: ## Start all services in development mode
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

restart: ## Restart all services
	docker-compose restart

shell-backend: ## Access backend container shell
	docker-compose exec backend /bin/bash

shell-db: ## Access database container shell
	docker-compose exec db psql -U postgres -d ticket_system

backup-db: ## Backup database
	docker-compose exec db pg_dump -U postgres ticket_system > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restore database (usage: make restore-db FILE=backup.sql)
	docker-compose exec -T db psql -U postgres ticket_system < $(FILE)

prod: ## Start in production mode
	docker-compose -f docker-compose.yml up -d --build

status: ## Show status of all services
	docker-compose ps
