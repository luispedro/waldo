<h2>Database Results</h2>
<p>Searched by {{ search_term_type }}(<strong>{{ search_term_value }}</strong>)
<table cellspacing="0" cellpadding="5" class="results">
<tr>
  <th>Protein</th>
  <th>Organism</th>
  <th>Celltype</th>
  <th>Condition</th>
  <th>GO Terms</th>
  <th>References (PubMed IDs)</th>
  <th>Evidence</th>
  <th>Evidence Code</th>
  <th>Original Entry Database</th>
</tr>

% for element in all_results:
<tr>
  <td>{{ element['protein'] }}</td>
  <td>{{ element['organism'] }}</td>
  <td>{{ element['celltype'] }}</td>
  <td>{{ element['condition'] }}</td>
  <td>{{ element['location'] }}</td>
  <td>{{ element['references'] }}</td>
  <td>{{ element['evidence'] }}</td> <!-- experiments, predictions ? -->
  <td>{{ element['evidence_code'] }}</td>
  <td>{{! element['source'] }}</td> <!-- original database -->
% end
</tr>
</table>

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

% rebase base title='Waldo'
