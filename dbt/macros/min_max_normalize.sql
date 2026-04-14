{% macro min_max_normalize(column, partition_by) %}
    coalesce(
      (cast({{ column }} as double) - min(cast({{ column }} as double)) over (partition by {{ partition_by }})) /
      nullif(max(cast({{ column }} as double)) over (partition by {{ partition_by }}) - min(cast({{ column }} as double)) over (partition by {{ partition_by }}), 0),
      0
    )
{% endmacro %}
