# Review classifier

Categorize feedback into pre-specified tags and categorizations.

---

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content. Predefined Categories: Product Features and Functionality Core Features Add-ons and Integrations Customization and Configuration User Experience and Design Ease of Use Navigation and Discoverability Visual Design and Aesthetics Accessibility Performance and Reliability Speed and Responsiveness Uptime and Availability Scalability Bug Fixes and Error Handling Customer Support and Service Responsiveness and Availability Knowledge and Expertise Issue Resolution and Follow-up Self-Service Resources Billing, Pricing, and Licensing Pricing Model and Tiers Billing Processes and Invoicing License Management Upgrades and Renewals Security, Compliance, and Privacy Data Protection and Confidentiality Access Control and Authentication Regulatory Compliance Incident Response and Monitoring Mobile and Cross-Platform Compatibility Mobile App Functionality Synchronization and Data Consistency Responsive Design Device and OS Compatibility Third-Party Integrations and API Integration Functionality and Reliability API Documentation and Support Customization and Extensibility Onboarding, Training, and Documentation User Guides and Tutorials In-App Guidance and Tooltips Webinars and Live Training Knowledge Base and FAQs |
| User   | I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

### Example output

> Categories:
>
> - Product Features and Functionality
>   - Core Features - Positive
>     User Experience and Design
>   - Ease of Use - Positive
>   - Visual Design and Aesthetics - Positive
> - Mobile and Cross-Platform Compatibility
>   - Mobile App Functionality - Negative
>   - Responsive Design - Negative
>   - Device and OS Compatibility - Negative
> - Third-Party Integrations and API
>   - Integration Functionality and Reliability - Negative
> - Customer Support and Service
>   - Responsiveness and Availability - Positive
>   - Issue Resolution and Follow-up - Positive

<CodeGroup>
    ```python Python
    import anthropic
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        temperature=1,
        system="You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript TypeScript
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });
    
    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1000,
      temperature: 1,
      system: "You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python AWS Bedrock Python
    from anthropic import AnthropicBedrock
    
    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()
    
    message = client.messages.create(
        model="anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=1000,
        temperature=1,
        system="You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript AWS Bedrock TypeScript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";
    
    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();
    
    const msg = await client.messages.create({
      model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens: 1000,
      temperature: 1,
      system: "You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python Vertex AI Python
    from anthropic import AnthropicVertex
    
    client = AnthropicVertex()
    
    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=1000,
        temperature=1,
        system="You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript Vertex AI TypeScript
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';
    
    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();
    
    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 1000,
      temperature: 1,
      system: "You are an AI assistant trained to categorize user feedback into predefined categories, along with sentiment analysis for each category. Your goal is to analyze each piece of feedback, assign the most relevant categories, and determine the sentiment (positive, negative, or neutral) associated with each category based on the feedback content.\n\nPredefined Categories:\n- Product Features and Functionality\n    - Core Features\n    - Add-ons and Integrations\n    - Customization and Configuration\n- User Experience and Design\n    - Ease of Use\n    - Navigation and Discoverability\n    - Visual Design and Aesthetics\n    - Accessibility\n- Performance and Reliability\n    - Speed and Responsiveness\n    - Uptime and Availability\n    - Scalability\n    - Bug Fixes and Error Handling\n- Customer Support and Service\n    - Responsiveness and Availability\n    - Knowledge and Expertise\n    - Issue Resolution and Follow-up\n    - Self-Service Resources\n- Billing, Pricing, and Licensing\n    - Pricing Model and Tiers\n    - Billing Processes and Invoicing\n    - License Management\n    - Upgrades and Renewals\n- Security, Compliance, and Privacy\n    - Data Protection and Confidentiality\n    - Access Control and Authentication\n    - Regulatory Compliance\n    - Incident Response and Monitoring\n- Mobile and Cross-Platform Compatibility\n    - Mobile App Functionality\n    - Synchronization and Data Consistency\n    - Responsive Design\n    - Device and OS Compatibility\n- Third-Party Integrations and API\n    - Integration Functionality and Reliability\n    - API Documentation and Support\n    - Customization and Extensibility\n- Onboarding, Training, and Documentation\n    - User Guides and Tutorials\n    - In-App Guidance and Tooltips\n    - Webinars and Live Training\n    - Knowledge Base and FAQs",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I've been using your email marketing platform for a few weeks, and I must say, the core features like campaign creation, email templates, and contact management are fantastic. The drag-and-drop editor makes it easy to design professional-looking emails, and the segmentation options help me target the right audience. However, I've had some issues with the mobile responsiveness of the emails. Some of my subscribers have reported that the layouts look broken on their smartphones, which is concerning. I'd love to see improvements in this area. Also, I noticed that the platform is missing some key integrations with popular CRM tools, which would be incredibly helpful for managing our leads and customers. On a positive note, the customer support team has been responsive and helpful whenever I've reached out with questions. Overall, it's a great tool, but there's definitely room for improvement in terms of mobile compatibility and third-party integrations."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>