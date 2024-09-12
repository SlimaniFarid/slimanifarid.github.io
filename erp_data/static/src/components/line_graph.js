/** @odoo-module */

import {Field} from '@web/views/fields/field';
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets"

const { onWillStart,useRef,onMounted, useState } = owl;


export class LineGraph extends Field {
    async setup() {
        super.setup();
        this.CyRef = useRef("main-cy");
        this.state = useState({ data:{}});
      onWillStart(async ()=>{
        let self = this
        self.state.data = self.props.value
        const JSfiles = ["/erp_data/static/src/lib/cytoscape.js",
                        "/erp_data/static/src/lib/dagre.js",
                        "/erp_data/static/src/lib/cytoscape-dagre.js",
                        "/erp_data/static/src/lib/sweetalert.js",
                      ];
        for (const file of JSfiles) {await loadJS(file);}
     
    })
    
      onMounted(async ()=>{
            let self = this
            self.get_line_graph()    
            
        })
    }

   get_line_graph(){
        let self = this
        let elements = JSON.parse(self.state.data)
        self.cy =   cytoscape({
            container: self.CyRef.el,
            zoom:2,
            elements : elements,
            style: [
                {
                 selector: 'node',
                 style: {
                    'background-color': '#3498db',
                    'label': 'data(name)',
                    'font-size': '12px',
                    'text-wrap': 'wrap'
                   }
                 },
                
                 {
                 selector: 'edge',
                 style: {
                    'label':'data(distance)',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#e74c3c',
                    'target-arrow-color': '#e74c3c',
                    'curve-style': 'bezier',
                    'text-background-color': '#ffffff',
                    'text-background-opacity': 1,
                    'text-background-padding': '4px'
                    
                   }
                 }
               ],
            layout: {
                name: 'dagre',
                rankDir: 'LR',
                directed: true,
                fit: true,
                spacingFactor: 2.5,
                animate: true,
              }
        });

       

        self.cy.on('tap', 'node', function(event) {
          let node = event.target;
          let sourceNodeId = '#'+self.cy.nodes()[0].data().id
          let targetNodeId = '#'+node.data().id
          let nodeIdsDistance = self.calculateTotalDistance(self.cy,sourceNodeId,targetNodeId)
          console.log('nodeIdsDistance=>',nodeIdsDistance)
          Swal.fire({
            title: node.data().name,
            html: "<strong><h3>PK :"+ nodeIdsDistance.distance.toFixed(2) + "</h3></strong>"+"<div>"+nodeIdsDistance.stations.join(" ➜ ")+"</div>",
            showConfirmButton: false,
            
          });
         
      });

   }

    calculateTotalDistance(cy,sourceNodeId,targetNodeId) {
        let path = cy.elements().aStar({root: sourceNodeId, goal: targetNodeId, directed: true}).path;
        let nodeIds = {"stations":[],'distance':0};
        if (path && path.length > 0) {
            for (var i = 0; i < path.length; i++) {
                let edge = path[i];
                if (edge.data().name!==undefined){
                    nodeIds.stations.push(edge.data().name)
                }
                if ( edge.data().distance !==undefined ){
                    console.log('edge.data().distance=>',edge.data().distance)
                    nodeIds.distance += edge.data().distance
                    }
                }
          }

        return nodeIds;
    }








}


LineGraph.template = 'erp_data.line_graph';

registry.category("fields").add("line_graph", LineGraph);
