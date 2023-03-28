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
  db_name        = var.DB_NAME
  db_user        = var.DB_USER
  db_password    = var.DB_PASS
}

# module "ecr" {
#   source = "../../modules/ecr"
# }

module "lb" {
  source                  = "../../modules/lb"
  vpc_id                  = module.vpc.vpc_id
  ecs_service_security_id = module.ecs.ecs_service_security_id
  public_subnet           = module.vpc.public_subnet
}

module "ecs" {
  source               = "../../modules/ecs"
  private_subnet       = module.vpc.private_subnet
  vpc_id               = module.vpc.vpc_id
  alb_target_group_arn = module.lb.alb_target_group_arn
}

module "route53" {
  source   = "../../modules/route53"
  alb      = module.lb.alb
  dns_name = var.ALB_DOMAIN
}