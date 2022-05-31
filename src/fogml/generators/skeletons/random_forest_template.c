{%- macro recurse(tree, node, depth, index) -%}
{%- set indent = "  " * depth -%}
{%- if tree["feature"][node] >= 0 -%}
{%- set name = tree["feature"][node] -%}
{%- set threshold = tree["threshold"][node] -%}
{{ indent }}if (x[{{ name }}] <= {{ '%0.10f' %threshold }}) {
{{ recurse(tree, tree["children_left"][node], depth + 1, index) }}
{{ indent }}}
{{ indent }}else {
{{ recurse(tree, tree["children_right"][node], depth + 1, index) }}
{{ indent }}}
{%- else -%}
{%- set class_index = argmax(tree["value"][node]) -%}
{{ indent }}results[{{ index }}] = {{ clf["classes_"][class_index] }};
{%- endif -%}
{%- endmacro -%}
int classify(float * x){
  int results[{{ clf["estimators_"]|length }}];
{%- set ns = namespace(index=0) -%}
{% for estimator in clf["estimators_"] %}
{% set tree = estimator.tree_ -%}
{{ recurse(tree, 0, 1, ns.index) }}
{%- set ns.index = ns.index + 1 -%}
{% endfor %}
  int classes_amount = 0;
  for(int i=0; i<{{ clf["estimators_"]|length }}; i++){
  	if(results[i]+1 > classes_amount) classes_amount = results[i]+1;
  }
  int result_class = -1;
  int max_apperance = 0;
  for(int i=0; i<classes_amount; i++){
    int apperance = 0;
    for(int j=0; j<{{ clf["estimators_"]|length }}; j++) if(results[j] == i) apperance++;
    if(apperance > max_apperance){
      max_apperance = apperance;
      result_class = i;
    }
  }
  return result_class;
