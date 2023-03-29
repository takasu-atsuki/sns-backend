module "vpc" {
  source    = "../../modules/vpc"
  elasticIp = module.ec2.elasticIp
}

module "ec2" {
  source = "../../modules/ec2"
}

# module "s3" {
#   source = "../../modules/s3"
# }

module "rds" {
  source         = "../../modules/rds"
  vpc_id         = module.vpc.vpc_id
  private_subnet = module.vpc.private_subnet
  public_subnet  = module.vpc.public_subnet
  db_name        = var.DB_NAME
  db_user        = var.DB_USER
  db_password    = var.DB_PASS
  db_port        = var.DB_PORT
}

# module "ecr" {
#   source                  = "../../modules/ecr"
#   ecr_repository_back     = var.ECR_REPOSITORY_BACK
#   ecr_repository_back_web = var.ECR_REPOSITORY_BACK_WEB
# }

module "lb" {
  source                  = "../../modules/lb"
  vpc_id                  = module.vpc.vpc_id
  ecs_service_security_id = module.ecs.ecs_service_security_id
  public_subnet           = module.vpc.public_subnet
  aws_region              = var.AWS_REGION
  aws_ssl_id              = var.AWS_SSL_ID
}

module "ecs" {
  source                = "../../modules/ecs"
  public_subnet         = module.vpc.public_subnet
  private_subnet        = module.vpc.private_subnet
  vpc_id                = module.vpc.vpc_id
  alb_target_group_arn  = module.lb.alb_target_group_arn
  ecs_task_role         = var.ECS_TASK_ROLE
  app_name              = var.ECR_REPOSITORY_BACK
  web_name              = var.ECR_REPOSITORY_BACK_WEB
  db_name               = var.DB_NAME
  db_host               = var.DB_HOST
  db_user               = var.DB_USER
  db_pass               = var.DB_PASS
  db_port               = var.DB_PORT
  front_url             = var.FRONT_URI
  arrowed_host          = var.ALLOWED_HOST
  aws_access_key_id     = var.AWS_ACCESS_KEYID
  aws_secret_access_key = var.AWS_SECRET_ACCESS_KEY
  aws_s3_backet_name    = var.AWS_S3_BACKET_NAME
  debug                 = var.DEBUG
  secret_key            = var.SECRET_KEY
}

module "route53" {
  source   = "../../modules/route53"
  alb      = module.lb.alb
  dns_name = var.ALB_DOMAIN
}