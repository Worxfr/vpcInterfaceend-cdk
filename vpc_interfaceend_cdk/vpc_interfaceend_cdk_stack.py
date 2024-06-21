from aws_cdk  import (
    Stack,
    aws_ec2 as ec2,
    Aws
) 

import aws_cdk as cdk

from constructs import Construct

class VpcInterfaceendCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC",
                      max_azs=1,
                      ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
                      subnet_configuration=[ec2.SubnetConfiguration(
                          subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                          name="Sub10",
                          cidr_mask=24
                      )]
        )

        vpc1cidr2 = ec2.CfnVPCCidrBlock(self, "VPCCIDR100",
            vpc_id=vpc.vpc_id,
            cidr_block="100.64.0.0/16"
        )

        private_subnet = ec2.CfnSubnet(self, "Sub100",
            availability_zone=vpc.availability_zones[0],
            cidr_block="100.64.0.0/24",
            vpc_id=vpc.vpc_id,
            tags= [cdk.CfnTag(key="Name", value=construct_id + "/VPC/SUB100")])
         
        private_subnet.add_dependency(vpc1cidr2)

        mySG = ec2.SecurityGroup(self, "security-group-VPCes",
            vpc=vpc,
            allow_all_outbound=True,
            description='CDK VPC Endp Security Group'
        )

        mySG.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), 'HTTPS frm anywhere')

        # add private endpoints for session manager
        ec2.CfnVPCEndpoint(self, 'ssm-vpce', 
            service_name="com.amazonaws."+Aws.REGION+".ssm",
            vpc_id=vpc.vpc_id,
            subnet_ids=[private_subnet.attr_subnet_id],
            security_group_ids=[mySG.security_group_id],
            vpc_endpoint_type='Interface',
            private_dns_enabled=True
        ).add_dependency(private_subnet)

        ec2.CfnVPCEndpoint(self, 'ssmmessages-vpce', 
            service_name="com.amazonaws."+Aws.REGION+".ssmmessages",
            vpc_id=vpc.vpc_id,
            subnet_ids=[private_subnet.attr_subnet_id],
            security_group_ids=[mySG.security_group_id],
            vpc_endpoint_type='Interface',
            private_dns_enabled=True
        ).add_dependency(private_subnet)

        ec2.CfnVPCEndpoint(self, 'ec2-vpce', 
            service_name="com.amazonaws."+Aws.REGION+".ec2",
            vpc_id=vpc.vpc_id,
            subnet_ids=[private_subnet.attr_subnet_id],
            security_group_ids=[mySG.security_group_id],
            vpc_endpoint_type='Interface',
            private_dns_enabled=True
        ).add_dependency(private_subnet)


        # Create an EC2 instance
        instance = ec2.Instance(self, "EC2Instance VPC1",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_filters=[ec2.SubnetFilter.by_cidr_ranges(["10.10.0.0/16"])])
        )




        
