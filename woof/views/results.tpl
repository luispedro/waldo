<p>Searched by {{ search_term_type }}(<strong>{{ search_term_value }}</strong>)

<h2>Database Results</h2>
% for element in all_results:
    <h3>{{ element['protein'] }} (in organism {{ element['organism'] }})</h3>
    <p>
    % if element['celltype'] is None:
        No cell type information<br />
    % else:
      In cell type <cite>{{ element['celltype'] }}</cite><br />
    % end
    % if element['condition'] is None:
        No condition information
    % else:
        In condition <cite>{{ element['condition'] }}</cite>
    % end
    </p>
    <p>Locations:</p>
    <ul>
    % for loc,ev in zip(element['location'], element['evidence_code']):
        <li>{{ loc }} ({{ ev }})</li>
    % end
    </ul>

  <p>References: {{ element['references'] }}</p>
  <p>Database Link: {{! element['source'] }}</p>
% end

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
