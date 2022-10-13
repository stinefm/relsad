---
title: 'RELSAD: A Python package for reliability assessment of modern distribution systems'
tags:
  - Python
  - Electrical engineering
  - Monte Carlo
  - Reliability
  - Smart grid
authors:
  - name: Stine Fleischer Myhre^[First author] # note this makes a footnote saying 'Co-first author'
    orcid: 0000-0002-2283-1724
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Olav Bjarte Fosso # note this makes a footnote saying 'Co-first author'
    affiliation: 1
    orcid: 0000-0002-3460-5839
  - name: Poul Einar Heegaard
    affiliation: 2
    orcid: 0000-0003-0083-5860
  - name: Oddbjørn Gjerde
    affiliation: 3
    orcid: 0000-0002-7978-747X
affiliations:
 - name: Department of Electric Power Engineering, NTNU, Trondheim, Norway
   index: 1
 - name: Department of Information Security and Communication Technology, NTNU, Trondheim, Norway
   index: 2
 - name: SINTEF Energy Research, Trondheim, Norway
   index: 3
date: 19 March 2022
bibliography: paper.bib

---

# Summary

The electrical power distribution system is under constant development and multiple changes will occur in the upcoming years. Through the integration of new technology such as Renewable Energy Resources (RES) and flexible resources such as microgrids, battery energy storage systems, and electrical vehicles, the distribution system becomes more active where bidirectional power flow is possible. In an active distribution system, utilization and control of the different sources are possible. Additionally, the system becomes smarter through the integration of Information and Communication Technology (ICT) where intelligent monitoring, automated control, and communication are possible. These changes increase the complexity of the distribution network and new dependencies and interdependencies in the system arise with the modernization of the system. 

The traditional reliability analysis methods for power systems do not consider the new components and technology, and the behavior and impact these have on the distribution network. Therefore, new considerations need to be taken to address these new changes in the system. 
This paper presents an open-source reliability assessment tool for smart and active distribution systems named `RELSAD`. 

`RELSAD` -- RELiability tool for Smart and Active Distribution networks is a Python-based reliability assessment tool that aims to function as a foundation for reliability calculation of modern distribution systems. RELSAD can be used by scientists, engineers, and Distribution System Operators (DSO) for the planning and operation of modern distribution system where the goal is to investigate the reliability of a given system. The tool allows for Monte Carlo simulation based reliability analysis of modern distribution networks, and sequential simulation of the network behavior with user-defined loading and failure evolution to investigate the impact of the introduction of for instance ICT components. The package supports user-selected time increment steps over a user-defined time period. In the tool, active components such as microgrids, distributed generation, batteries, and electrical vehicles are implemented. To evaluate smart power systems, ICT components such as automated switches, sensors, and control system for the power grid are also implemented. In addition to component implementation, in order to evaluate the reliability of such complex systems, the complexity, dependencies within a system, and interdependencies between systems and components are accounted for. 

`RELSAD` offers the following features:

* A foundation for calculating the reliability of modern distribution systems with smart and active components that account for the increased complexity of the system. 

* An extensive reliability analysis foundation with important and new reliability indices that aims to give a complete picture of the reliability of both the power system and the components in the system.

* Inclusion of active participation of different power sources such as distributed generation, microgrids and batteries.

* Inclusion of ICT system and components and the interdependencies between the ICT and power systems.

# Statement of need

One of the most important tasks of the DSO is to ensure a safe operation of the power system where the needed electrical power reaches the end-users. With the increased complexity of the system, new situations affecting the distribution system reliability will occur. Power system reliability addresses the issues of interruption in service and the loss of power supply. The traditional reliability analysis methods for distribution systems do not fully comprehend the increased complexity in the system and do not account for the structural changes and time dependencies brought by, for example, RES and ICT. With the increased penetration of RES with power that vary over time, analyzing the power system under varying conditions is important for the reliability of the system. 

In literature, reliability evaluation of distribution systems is conducted either through analytical approaches or by simulation. @Billinton:1992 have been pioneers in power system reliability and describe multiple analytical approaches for evaluating the reliability of distribution systems. In an analytical approach, a mathematical representation of the distribution system is constructed by evaluating the components and the relation between them. Markov models can be applied to capture the dynamics in the system behavior. An alternative approach, RELRAD -- an analytical approach for distribution system reliability assessment, uses the fault contribution from all the power system components to calculate the individual load point reliability in a radially operated system [@Kjølle:1992]. However, these methods consider passive operation of the network and are therefore not optimal when analyzing modern distribution systems. 

Simulation gives a more accurate representation of a modern system where active networks are to be considered. In [@escalera:2018], Monte Carlo simulation is highlighted as a good approach for evaluating the reliability of modern power systems. In addition, the paper points out the need for new reliability assessment tools for such systems. In such a tool, the dynamics and the interconnection of the system can be studied. There is some literature that has used Monte Carlo simulation as a method to evaluate the reliability of modern distribution systems [@celli:2013; @de:2017; @borges:2012]. However, the literature does not bring forward a general and open method or tool for the reliability assessment of modern distribution systems. 

The reliability of the distribution system is often described through customer-oriented indices. The customer-oriented indices aim to indicate the reliability of the distribution system based on the interruption experienced by the customers in the system. Some of the most commonly used indices are the System Average Interruption Frequency Index (SAIFI) which gives the average experienced interruption for the customers and the System Average Interruption Duration Index (SAIDI) which gives the average experienced duration of interruption for the customers. Additionally, indices such as Energy not Supplied and component-oriented indices which for example give the expected availability of the component, are also common to use. In RELSAD, multiple indices are implemented in order to give the user a great opportunity for reliability analysis. 

`RELSAD` is a simulation tool that uses Monte Carlo simulations for the reliability assessment of distribution systems. The tool is based upon some principles from the analytical approach RELRAD when calculating the individual load point reliability of the system. Compared to the traditional methods, `RELSAD` comprehends the complexity and time dependencies that arise in modern distribution systems.  


# Package structure

`RELSAD` consists of an electric power system model and an ICT system model that constitutes the system network model.
\autoref{fig:structure} gives an overview of how the systems and components in `RELSAD` are structured. In addition, the connection between the components and networks is illustrated. The user builds up one network or several networks or can use the implemented test networks. In the distribution network, components such as lines, buses, and switches (discounters and circuit breakers) can be added to make the system topology. In addition to the distribution network, an ICT network can be constructed and connected to the distribution system through ICT components. The implemented ICT components are illustrated in \autoref{fig:structure}. The sensors can be placed on the electrical lines in the distribution system, and will then be able to monitor the line. The intelligent switch can be placed on disconnectors in the system to allow for automated control of the switch. Through an ICT network, the sensor and the intelligent switch can communicate with the controller (data center) representing the operation center of the DSO. 

The components in the network can be assigned reliability data were given specifications of the components can be decided. Additionally, the user is free to set the load and generation profiles for the loads and generation units in the network. The user can then select the time increment and period of the simulation. 

![The structure of the systems and components in `RELSAD`.\label{fig:structure}](SystemStructure.pdf)

# Acknowledgements

This work is funded by CINELDI - Centre for intelligent electricity distribution, an 8-year Research Centre under the FME-scheme (Centre for Environment-friendly Energy Research, 257626/E20). 
The authors gratefully acknowledge the financial support from the Research Council of Norway and the CINELDI partners.  

This research is a part of an ongoing PhD project. 

# References

