variable "project_id" {
    default = "project-8275"
  }
  
  variable "source_image_family" {
    default = "centos-stream-8"
  }
  
  variable "ssh_username" {
    default = "centos"
  }
  
  variable "zone" {
    default = "europe-west4-a"
  }
  
  variable "image_name" {
    default = "webapp-custom-image"
  }
  
  variable "public_ssh_key_path" {
    default = "/Users/raviirt/.ssh/id_rsa.pub"
  }
  
  packer {
    required_plugins {
      googlecompute = {
        source  = "github.com/hashicorp/googlecompute"
        version = "~> 1"
      }
    }
  }
  
  source "googlecompute" "example" {
    project_id         = var.project_id
    source_image_family = var.source_image_family
    ssh_username       = var.ssh_username
    zone               = var.zone
  
  metadata={
    ssh-keys= "centos:${var.public_ssh_key_path}"
  }

    disk_size      = 20
    disk_type      = "pd-standard"
    network        = "default"
    communicator   = "ssh"
  }
  
  build {
    sources = ["source.googlecompute.example"]
  
    provisioner "shell" {
      script = "provision.sh"
    }
  }
  