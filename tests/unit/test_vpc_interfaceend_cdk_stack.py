import aws_cdk as core
import aws_cdk.assertions as assertions

from vpc_interfaceend_cdk.vpc_interfaceend_cdk_stack import VpcInterfaceendCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in vpc_interfaceend_cdk/vpc_interfaceend_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VpcInterfaceendCdkStack(app, "vpc-interfaceend-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
