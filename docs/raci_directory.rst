RACI Stakeholder Directory
==========================

.. raw:: html

   <section class="raci-directory-admin">
     <div class="raci-directory-form">
       <div>
         <div class="micro-label">Governance Provisioning</div>
         <h2>Stakeholder Administration</h2>
         <p>Provision owners, reviewers, and informed stakeholders into the KPI governance matrix. This form is an interface scaffold for the offline governance registry.</p>
       </div>
       <form class="raci-provision-form">
         <label>
           <span>Employee Name</span>
           <input type="text" placeholder="e.g. Finance Data Owner">
         </label>
         <label>
           <span>Corporate Email</span>
           <input type="email" placeholder="name@enterprise.example">
         </label>
         <label>
           <span>Employee ID No</span>
           <input type="text" placeholder="LEAP-000000">
         </label>
         <label>
           <span>Role Tier</span>
           <select>
             <option>Accountable</option>
             <option>Responsible</option>
             <option>Consulted</option>
             <option>Informed</option>
           </select>
         </label>
         <button type="button">Provision Stakeholder</button>
       </form>
     </div>

     <div class="raci-directory-table-wrap">
       <table class="raci-directory-table">
         <thead>
           <tr>
             <th>Employee Name</th>
             <th>Corporate Email</th>
             <th>Employee ID No</th>
             <th>Assigned KPIs</th>
             <th>Role Tier</th>
           </tr>
         </thead>
         <tbody>
           <tr><td><strong>Enterprise Data Owner</strong></td><td><code>enterprise.data.owner@enterprise.example</code></td><td><code>LEAP-800575</code></td><td>Cooling Water Delta-T (°C), On-Spec Rate (%), Polymer Melt Flow Index (MFI) Variance, Propylene to Ethylene (P/E) Ratio</td><td><span class="raci-badge raci-a">A</span>Decision Owner</td></tr><tr><td><strong>Finance Data Owner</strong></td><td><code>finance.data.owner@enterprise.example</code></td><td><code>LEAP-563025</code></td><td>Maintenance to Operating Cost Ratio, Specific Catalyst Cost ($/ton)</td><td><span class="raci-badge raci-a">A</span>Decision Owner</td></tr><tr><td><strong>HSE Data Owner</strong></td><td><code>hse.data.owner@enterprise.example</code></td><td><code>LEAP-E8A7C7</code></td><td>SOx Emissions Concentration (kg/m3), kpi flare recovery pct</td><td><span class="raci-badge raci-a">A</span>Decision Owner</td></tr><tr><td><strong>Maintenance Data Owner</strong></td><td><code>maintenance.data.owner@enterprise.example</code></td><td><code>LEAP-67436D</code></td><td>Mean Time Between Failures (MTBF)</td><td><span class="raci-badge raci-a">A</span>Decision Owner</td></tr><tr><td><strong>Operations Data Owner</strong></td><td><code>operations.data.owner@enterprise.example</code></td><td><code>LEAP-5F7901</code></td><td>Daily Feedstock Throughput (tons/day), OEE %, Yield Percentage (%)</td><td><span class="raci-badge raci-a">A</span>Decision Owner</td></tr><tr><td><strong>Domain Subject Matter Expert</strong></td><td><code>domain.subject.matter.expert@enterprise.example</code></td><td><code>LEAP-35DF31</code></td><td>Cooling Water Delta-T (°C), On-Spec Rate (%), Polymer Melt Flow Index (MFI) Variance, Propylene to Ethylene (P/E) Ratio</td><td><span class="raci-badge raci-c">C</span>Subject Matter Reviewer</td></tr><tr><td><strong>Environmental Compliance Team</strong></td><td><code>environmental.compliance.team@enterprise.example</code></td><td><code>LEAP-D03578</code></td><td>SOx Emissions Concentration (kg/m3), kpi flare recovery pct</td><td><span class="raci-badge raci-c">C</span>Subject Matter Reviewer</td></tr><tr><td><strong>Finance BI Team</strong></td><td><code>finance.bi.team@enterprise.example</code></td><td><code>LEAP-A01205</code></td><td>Maintenance to Operating Cost Ratio, Specific Catalyst Cost ($/ton)</td><td><span class="raci-badge raci-c">C</span>Subject Matter Reviewer</td></tr><tr><td><strong>Process Engineering Team</strong></td><td><code>process.engineering.team@enterprise.example</code></td><td><code>LEAP-4B10D7</code></td><td>Daily Feedstock Throughput (tons/day), OEE %, Yield Percentage (%)</td><td><span class="raci-badge raci-c">C</span>Subject Matter Reviewer</td></tr><tr><td><strong>Reliability Engineering Team</strong></td><td><code>reliability.engineering.team@enterprise.example</code></td><td><code>LEAP-8B4B07</code></td><td>Mean Time Between Failures (MTBF)</td><td><span class="raci-badge raci-c">C</span>Subject Matter Reviewer</td></tr><tr><td><strong>Business Stakeholders</strong></td><td><code>business.stakeholders@enterprise.example</code></td><td><code>LEAP-4D9F00</code></td><td>Cooling Water Delta-T (°C), On-Spec Rate (%), Polymer Melt Flow Index (MFI) Variance, Propylene to Ethylene (P/E) Ratio</td><td><span class="raci-badge raci-i">I</span>Executive Observer</td></tr><tr><td><strong>CFO Office</strong></td><td><code>cfo.office@enterprise.example</code></td><td><code>LEAP-0D24DB</code></td><td>Maintenance to Operating Cost Ratio, Specific Catalyst Cost ($/ton)</td><td><span class="raci-badge raci-i">I</span>Executive Observer</td></tr><tr><td><strong>HSE Leadership</strong></td><td><code>hse.leadership@enterprise.example</code></td><td><code>LEAP-7E6992</code></td><td>SOx Emissions Concentration (kg/m3), kpi flare recovery pct</td><td><span class="raci-badge raci-i">I</span>Executive Observer</td></tr><tr><td><strong>Maintenance Leadership</strong></td><td><code>maintenance.leadership@enterprise.example</code></td><td><code>LEAP-CC3D60</code></td><td>Mean Time Between Failures (MTBF)</td><td><span class="raci-badge raci-i">I</span>Executive Observer</td></tr><tr><td><strong>Plant Management</strong></td><td><code>plant.management@enterprise.example</code></td><td><code>LEAP-404DBA</code></td><td>Daily Feedstock Throughput (tons/day), OEE %, Yield Percentage (%)</td><td><span class="raci-badge raci-i">I</span>Executive Observer</td></tr><tr><td><strong>Data Engineering Team</strong></td><td><code>data.engineering.team@enterprise.example</code></td><td><code>LEAP-141BCB</code></td><td>Cooling Water Delta-T (°C), On-Spec Rate (%), Polymer Melt Flow Index (MFI) Variance, Propylene to Ethylene (P/E) Ratio</td><td><span class="raci-badge raci-r">R</span>Execution Owner</td></tr><tr><td><strong>Environmental Data Engineering Team</strong></td><td><code>environmental.data.engineering.team@enterprise.example</code></td><td><code>LEAP-4BDDA5</code></td><td>SOx Emissions Concentration (kg/m3), kpi flare recovery pct</td><td><span class="raci-badge raci-r">R</span>Execution Owner</td></tr><tr><td><strong>Finance Data Engineering Team</strong></td><td><code>finance.data.engineering.team@enterprise.example</code></td><td><code>LEAP-5B3862</code></td><td>Maintenance to Operating Cost Ratio, Specific Catalyst Cost ($/ton)</td><td><span class="raci-badge raci-r">R</span>Execution Owner</td></tr><tr><td><strong>Operations Data Engineering Team</strong></td><td><code>operations.data.engineering.team@enterprise.example</code></td><td><code>LEAP-7B3EEF</code></td><td>Daily Feedstock Throughput (tons/day), OEE %, Yield Percentage (%)</td><td><span class="raci-badge raci-r">R</span>Execution Owner</td></tr><tr><td><strong>Reliability Data Engineering Team</strong></td><td><code>reliability.data.engineering.team@enterprise.example</code></td><td><code>LEAP-91C3F8</code></td><td>Mean Time Between Failures (MTBF)</td><td><span class="raci-badge raci-r">R</span>Execution Owner</td></tr>
         </tbody>
       </table>
     </div>
   </section>
