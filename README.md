# senate-voting-application
Project Description 
This is a major assessment component that expects students to join a team and carry out a project consisting of different tasks assessable at the individual as well as group levels. The project tasks purport to design and prototype a software system by following security by design paradigm and principles. The project aims to provide the students with an opportunity demonstrate the knowledge, understanding, and skills gained from the material covered in this course. The project’s tasks will ony be accepted if the following “gold standard” security elements are incorporated in the design and implementation of the system: Authentication. The system must authenticate its users and/or allow its users to authenticate the system. Users may include human users as well as programs executing on machines. You must implement reasonable means of authentication, which may include passwords, user registration, secrets generation, key distribution, etc. Authorization. The system must enforce some authorization policy to control some subset of its operation. Implement an access control mechanism that is appropriate and natural for your system’s functionality and expected scale. Audit. The system must provide infrastructure for audit or other means of establishing accountability for actions. Confidentiality and Integrity. The system must involve information that resides in long-term storage or that is transmitted over a network. The system’s mission must require that information to be kept secret and/or be protected from corruption. The list of the essential security elements above defines only a subset of the security functionality your project will be implemented. This list is not meant to be exhaustive; you are encouraged to explore the other aspects of secure software engineering. The project is specified below. Electronic Senate Voting System The final group project description may be familiar to some of the students who have already taken Engineering Software as Services I, but this course shifts the focus to non-trivial security functionality and software reliability. The project is to implement a web-based voting system for the Australian Senate. This top-secret AEC project will allow a state's AEC Commissioner's delegate(s) to enter the details of the candidates, including their order within their party grouping. It will allow individual voters to enter their votes either above the line, below the line but not both. It will correctly calculate the order in which senators should be elected. It will also allow the state's AEC Commissioner's delegate(s) to manually exclude candidates if a recount should be ordered by the High Court sitting as the Court of Disputed Returns.

# Requirements

    * pip3
    * python3

# To run this application:

    * Ensure you have Python and PIP installed
    * Navigate to ADMIN folder
      * Run "pip3 install ." into a termainal in the ADMIN folder
      * Run "python3 app.py"
      * Access it through localhost:5000
    * Navigate to VOTER folder
      * Run "pip3 install ." into a termainal in the VOTER folder
      * Run "python3 app.py"
      * Access it through localhost:5001

