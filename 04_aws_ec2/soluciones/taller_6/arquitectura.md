

flowchart TD

&#x20;   A\[Internet] --> B\[Application Load Balancer]



&#x20;   subgraph ASG\["Auto Scaling Group - Subredes privadas"]

&#x20;       C\["EC2-1 - Flask - AZ A"]

&#x20;       D\["EC2-2 - Flask - AZ B"]

&#x20;       E\["EC2-3 - Flask - AZ C"]

&#x20;   end



&#x20;   B --> C

&#x20;   B --> D

&#x20;   B --> E



&#x20;   C --> F\[(Amazon RDS)]

&#x20;   D --> F

&#x20;   E --> F



