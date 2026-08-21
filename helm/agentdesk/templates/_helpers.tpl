{{- define "agentdesk.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "agentdesk.fullname" -}}
{{- .Release.Name }}-{{ include "agentdesk.name" . }}
{{- end }}
