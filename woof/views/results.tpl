<p>Results for <cite>{{ search_term_value }}</cite> as {{ search_term_type }}</p>

<h2>Summary Overview</h2>

<p>This is a summary of what we found after mapping to the <a
href="http://www.geneontology.org/GO.slims.shtml#whatIs">GO Slim</a> defined by
<a href="http://www.informatics.jax.org/">Mouse Genome Informatics</a></p>:

<table id="goslim_results">
<tr id="goslim_results_header">
<th>Location</th>
% for key in goslim:
    <th>{{ key }}</th>
% end
</tr>
% for p in goslim_all:
    <tr>
    <td class="goslim_results_location">{{ p }}</td>
    % for key in goslim:
        % if p in goslim[key]:
            <td>YES</td>
        % else:
            <td>NO</td>
        % end
    % end
    </tr>
% end
</table>

<style>
#goslim_results TD {
    padding-left: 2em
    padding-right: 3em
}
.goslim_results_location {
    padding-right: 4em
}
#goslim_results_header {
    border-bottom: 2px solid black;
    background: #eee;
}
#goslim_results {
    border-top: 2px solid black;
    border-bottom: 2px solid black;
    margin-left: 120px; 
}

</style>

<p><em>Note that these databases are not independent sources as information
from one database can be used as the basis for another database.</em></p>

<h2>Database Results</h2>
% for element in all_results:
    <div class="dbresult">
    <h3>{{ element['protein'] }}</h3>
    <p>
    % if element['celltype'] is not None:
      In cell type <cite>{{ element['celltype'] }}</cite><br />
    % end
    % if element['condition'] is not None:
        In condition <cite>{{ element['condition'] }}</cite>
    % end
    </p>
    <p>Listed Locations:</p>
    <ul>
    % for loc,ev in element['location']:
        <li>{{ loc }}
        % if ev is not None:
            ({{ ev }})
        % end
        </li>
    % end
    </ul>

    % if element['references']:
        <p>References:</p>
        <ul>
        % for p in element['references']:
            <li>{{! p.gen_citation() }}</li>
        </ul>
        %end
    % end
    <p>Database link: {{! element['source'] }}</p>
    </div>
% end

% if PREDICTIONS_ENABLED:

    <h2>Prediction Results</h2>
    % if predictions:
        % for pred in predictions:
            <p>Prediction algorithm: {{pred[0] }}
                <ul>
                % for r in pred[1]:
                    <li>{{r.prediction}} ({{r.strength}})</li>
                % end
                </ul>
        % end
    % else:
        <p>No prediction for this protein.</p>
    % end
% end


% rebase base title='Waldo'
