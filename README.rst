######
RELSAD
######

.. overview_start

`RELSAD` -- RELiability tool for Smart and Active Distribution networks,
is a Python-based reliability assessment tool that aims to function as
a foundation for reliabilitycalculation of modern distribution systems.
The tool allows for Monte Carlo simulation based reliability analysis of modern
distribution networks, and sequential simulation of the network
behavior with user-defined loading and failure evolution to investigate the impact
of the introduction of for instance ICT components.


The package supports user-selected time steps over a user-defined time period.
In the tool, active components such as microgrids, distributed generation,
batteries, and electrical vehicles are implemented.
To evaluate smart power systems, ICT (Information and Communication Technology)
components such as automated switches, sensors, and control systems
for the power grid are also implemented.
In addition to component implementation, in order to evaluate the reliability
of such complex systems, the complexity, dependencies within a system, and interdependencies between systems and components are accounted for.

The tool can be used in modern distribution network development to evaluate
the influence of active components on the network reliability. Relevant use cases
include investigating how:

1. The introduction of microgrids with active generation
   affects the customers in the distribution network and vice versa
2. Vehicle\-to\-grid strategies might mitigate load peaks and
   improve the distribution network reliability
3. The reliability of the ICT network impacts the
   distribution network reliability

.. overview_end

============
Installation
============

See https://relsad.readthedocs.io/en/latest/installation.html.

========
Features
========

- Monte Carlo simulation based reliability analysis of modern distribution networks
- Sequential simulation of the network behavoir with user-defined loading and failure evolution

============
Dependencies
============

The package dependencies can be found in `pyproject.toml`.

=====
Usage
=====

Examples using well known test networks are included and presented in
https://relsad.readthedocs.io/en/latest/usage.html.

=============
Documentation
=============

The official documentation is hosted on Read the Docs: https://relsad.readthedocs.io/en/latest/

============
Contributors
============

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://img.shields.io/github/contributors/stinefm/relsad).


====
Help
====

If you have questions, feel free to contact the author.

