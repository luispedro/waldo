<p>Results for <cite>{{ search_term_value }}</cite> as {{ search_term_type }}</p>

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
    % for loc,ev in zip(element['location'], element['evidence_code']):
        <li>{{ loc }} ({{ ev }})</li>
    % end
    </ul>

    % if element['references']:
        <p>References: {{ element['references'] }}</p>
    % end
    <p>Database link: {{! element['source'] }}</p>
    </div>
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
