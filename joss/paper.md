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
    orcid: 0000-0000-0000-0000
  - name: Poul Einar Heegaard
    affiliation: 2
    orcid: 0000-0000-0000-0000
  - name: Oddbjørn Gjerde
    affiliation: 3
    orcid: 0000-0000-0000-0000
affiliations:
 - name: Department of Electric Power Engineering, NTNU, Trondheim, Norway
   index: 1
 - name: Department of Information Security and Communication Technology, NTNU, Trondheim, Norway
   index: 2
 - name: SINTEF Energy Research, Trondheim, Norway
   index: 3
date: 19 March 2022
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
#aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
#aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

With increased penetration of new technology in the electrical power systems such as Renewable Energy Resources, flexible resources, and Information and Communication Technology (ICT), the power systems become more complex and with more dependencies. 
The traditional reliability analysis methods for power systems do not consider the new components and technology, therefore, new considerations need to be taken to address these new changes in the system. 
This paper presents an open-source reliability assessment tool for smart and active distribution systems named `RELSAD`. 

`RELSAD` -- RELiability tool for Smart and Active Distribution networks, is a Python-based reliability assessment tool that aims to function as a foundation for reliability calculation of modern distribution systems. 
<!--`RELSAD` is a Python-based package tool that aims to function as a foundation for reliability calculation for smart and active distribution systems. -->
The tool uses Monte Carlo simulation and stochastic variation to simulate the reliability of a distribution system. The package supports user-selected time increment steps over a user-defined time period. In the tool, active components such as microgrids, wind power, solar power, batteries, and electrical vehicles are implemented. To evaluate smart power systems, ICT components such as automated switches, sensors, and control system for the power grid are also implemented. In addition to component implementation, in order to evaluate the reliability of such complex systems, the complexity, dependencies within a system, and interdependencies between systems and components are accounted for. 

<!--- the dependencies between the different components and networks are included. --->

`RELSAD` offers the following features:

* A foundation for calculating the reliability of modern distribution systems with smart and active components that account for the increased complexity in the power system. 

* An extensive reliability analysis foundation with important and new reliability indices that aims to give a complete picture of the reliability of both the power system and the components in the system.

* Inclusion of active participation of different power sources such as distributed generation, microgrids and batteries. <!--A simulation tool that includes active participation of different power sources such as distributed generation, microgrids, and batteries. -->

* Inclusion of ICT system and the interdependencies between the ICT and power systems. <!---A simulation tool that includes ICT components and the dependency between the ICT components and the power system.--> 



<!---In `RELSAD` active components such as microgrids, wind power, solar power, and electrical vehicles are implemented. In addition, a communication network with smart ICT components are implemented in the tool. 
The tool is made as a Python package built up based on an object-oriented programming approach. --->

# Statement of need

One of the most important tasks of the Distribution System Operator is to ensure a safe operation of the power system where the needed electrical power reaches the end-users. With the increased complexity of the system, new situations affecting the reliability will occur. The traditional reliability analysis methods for distribution systems do not fully comprehend the increased complexity in the system and do not account for the structural changes and time dependencies brought by, for example, Renewable Energy Resources and ICT. With the increased penetration of renewable energy sources with power that vary over time, analyzing the power system under varying conditions is important for the reliability of the system. 


<!---do not consider the changes occurring in the distribution system. Typically, only passive operation of distribution systems, often without the presence of generation units, is considered. If a generation unit is present, the unit will not participate in the analysis in an active manner, and will be disconnected during the fault period of the distribution system.  --->

In literature, reliability evaluation of distribution systems is conducted either through analytical approaches or by simulation. @Billinton:1992 have been pioneers in power system reliability and describe multiple analytical approaches for evaluating the reliability of distribution systems. In an analytical approach, a mathematical representation of the distribution system is constructed by evaluating the components and the relation between them. Markov models can be applied to capture the dynamics in the system behavior. An alternative approach, RELRAD -- an analytical approach for distribution system reliability assessment, uses the fault contribution from all the power system components to calculate the individual load point reliability in a radially operated system [@Kjølle:1992]. However, these methods consider passive operation of the network and are therefore not optimal when analyzing modern distribution systems. 


<!---To capture the dynamics in the system behavior, Markov models can be applied. From the state models, both transient and stationary properties can be extracted, such as the availability and the reliability of the system. To capture the structure and the interrelation between the system components, Markov models are not scalable. Alternatively, the system can be represented by a structural model (such as Reliability Block Diagrams and Fault trees), from which minimal cut sets can be defined and stationary system properties can be determined.
Another analytical approach, RELRAD, uses the fault contribution from all the network components to calculate the individual load point reliability in the system [@Kjølle:1992]. However, these methods consider the passive operation of the network and are therefore not optimal when analyzing modern distribution systems. --->

Simulation gives a more accurate representation of a modern system where active networks are to be considered. In [@escalera:2018], Monte Carlo simulation is highlighted as a good approach for evaluating the reliability of modern power systems. In addition, the paper points out the need for new reliability assessment tools for such systems.  Here, the dynamics and the interconnection of the system can be studied. There is some literature that has used Monte Carlo simulation as a method to evaluate the reliability of modern distribution systems [@celli:2013; @de:2017; @borges:2012]. However, the literature does not bring forward a general and open method or tool for the reliability assessment of modern distribution systems. 

`RELSAD` is a simulation tool that uses Monte Carlo simulations for the reliability assessment of distribution systems. The tool is based upon some principles from the analytical approach RELRAD when calculating the individual load point reliability of the system. Compared to the traditional methods, `RELSAD` comprehends the complexity and time dependencies that arise in modern distribution systems.  


<!--- `Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike. --->

# Package structure


<!--In this section, we provide a brief overview over the structure and functionality of the package. -->


`RELSAD` consists of an electric power system model and an ICT system model that constitutes the system network model. <!---is built up by differentiating between the electrical power system and the ICT system of a network model. --> 
\autoref{fig:structure}, gives an overview of how the systems and components in `RELSAD` are structured. In addition, the connection between the components and networks is illustrated. The user builds up one network or several networks or can use the implemented test networks. Components can be added to the network where reliability data and specifications of the components can be set. The user can then select the time increment and period of the simulation. 


![The structure of the systems and components in `RELSAD`.\label{fig:structure}](SystemStructure.pdf)



<!---
Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"


Summary: Has a clear description of the high-level functionality and purpose of the software for a diverse, non-specialist audience been provided?
A statement of need: Does the paper have a section titled 'Statement of Need' that clearly states what problems the software is designed to solve and who the target audience is?
State of the field: Do the authors describe how this software compares to other commonly-used packages?
Quality of writing: Is the paper well written (i.e., it does not require editing for structure, language, or writing quality)?
References: Is the list of references complete, and is everything cited appropriately that should be cited (e.g., papers, datasets, software)? Do references in the text use the proper citation syntax?

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% } ---> 

# Acknowledgements

This work is funded by CINELDI - Centre for intelligent electricity distribution, an 8-year Research Centre under the FME-scheme (Centre for Environment-friendly Energy Research, 257626/E20). 
The authors gratefully acknowledge the financial support from the Research Council of Norway and the CINELDI partners.  

This research is a part of an ongoing PhD project. 



# References

