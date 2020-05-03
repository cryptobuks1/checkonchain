# Decred Proposal

## Introduction

Decred has a growing team of research analysts and a suite of on-chain performance and pricing metrics that have been developed in the last 12 months. A common feedback item on social channels is where can the community find these charts to study and interrogate the data in real time. Examples of sites which fullfil this role for Bitcoin are [Woobull.com](http://charts.woobull.com/), [lookintobitcoin](https://www.lookintobitcoin.com/charts/), [Digitalik.net](https://digitalik.net/btc/), and [Glassnode](https://studio.glassnode.com/metrics).

This proposal updates/follows on from [Part 1 of Checkmate's Phase 2 proposal (dcrdata specs)](https://proposals.decred.org/proposals/a677e236cb2e0fdd485980cd5d789e668d00fdc5235d01e7345d2195b8679066). As discussed in Matrix Proposals channel, it was agreed that these charts are better presented outside the explorer for a number of reasons including scarce dcrdata/DEX dev time, ability to innovate faster without fear of breaking the explorer and the 'formal/informal' balance where we don't want 'speculative' trading metrics presented on a Decred project core resource. 

## What
This proposal aims to deliver an MVP website that will host live charts for Decred performance metrics as well as a research hub containing the relevant research papers and blog developed by research analysts. The purpose of the site is the following:

- Provide a resource for stakeholders to interrogate Decred performance based on near-real time data to enhance governance decision making.

- Provide traders and investors (retail and Institutions) with a tool to make market decisions. Ideally, this will also demonstrate that tradeable signals do exist for DCR and has potential to be a draw for more liquidity as traders take advantage of the information asymmetry.

- Create an education resource aggregating Decred charts, research papers and recorded videos of explainers/seminars etc which discuss the content and application of the above.

It is proposed to build the website in phases with this proposal covering the following MVP Features (Phase 1):

1. 5 live charts as specified in [this git-repo](https://github.com/checkmatey/checkonchain/blob/master/research_articles/checkonchain_charts/checkonchain_charts.md) (MVRV Ratio, Stakeholder commitments in USD and BTC, NVT/RVT Ratio, Mayer Multiple, 142-day Ticket Sum). Charts will be switchable between light and dark modes. It is expected there will be three umbrella categories for the charts 
    
    a) Pricing models (block subsidy, 142-day Ticket Sum)

    b) Oscillators (Mayer multiple and NVT/RVT ratio)

    c) Performance metrics (charts looking at various performance metrics like privacy mixing, cumulative fees, fee ratios etc)

2. An education hub with blog, curated research paper archive and hosting of recorded video explainers.

3. Language support for English and Spanish to start.

Following delivery of the MVP, additional work phases can be progressed to expand the scope and content of the site to include additional charts, research, languages, network dashboards etc. It is suggested that equivalent charts for Bitcoin be presented in a later stage, subject to stakeholder discussion. The reason being that if the charts/research are found to be useful outside the Decred community, it has the potential to draw market share from the competition above and brings more eyes onto Decred, as people using the Bitcoin charts/research are only one click away.

**Two prototype layouts** ([WIP_1](https://xd.adobe.com/view/efae9a9b-a5e3-4bf2-4723-8d3f0a0e2aee-999f/) and [WIP_2](https://projects.invisionapp.com/share/ACX4905MNWX#/screens/416016812) have been prepared to demonstrate the current design concepts.

## Who

The assembled team for this project are:

- Research and chart code: checkmate and permabull nino
- Design: nachito and stanvl
- Web-dev: pablito and svitekpavel

## How

**Research/documentation** - Each chart will have a small blurb with links to the author and more detailed research papers/references.

**Chart Development** - [code backend is largely written](https://github.com/checkmatey/checkonchain/blob/master/dcronchain/charts/dcr_charts.py) already by checkmate in python using plotly, coinmetrics and dcrdata. pablito and svitekpavel are assisting with integration with the web-dev backend.

**Design** - 

**Web-Dev** - 


## Budget Requested

**Research/documentation/charts $0** - The work completed by checkmate/nino to date on [Phase 2 Part 1](https://proposals.decred.org/proposals/a677e236cb2e0fdd485980cd5d789e668d00fdc5235d01e7345d2195b8679066) is directly relevant and feeds into this proposal such that no additional time/budget is necessary for these contributions. What is requested is for checkmate to re-allocate 33%-50% of his time/budget from his Part 1 research proposal ($5k to $7.5k) to completing the documentation / new research papers dedicated to the site. This will detail how each chart is presented and applied, how the indicators relate to Decred fundamentals and what these signals mean in practice. This can also include video recorded explainers for the 5 MVP charts.


**Design $XX** - 

**Web-Dev $XX** - 

## For Discussion

The working title of the project is **Checkonchain** (a hangover from what checkmate called his codebase repo). The name has relevance to what it achieves but also obviously has the front of authors pseudonym in it and he doesn't want to enshrine himself unnecessarily. Thus, if the community has suggestions for suitable names for the project, please let us know in the comments.


