source <(grep -v '^#' .env | sed 's/^/export /')
git config user.email "callensxavier@gmail.com"
git config user.name "Xavier Callens"
git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter.git
git checkout -b feature/workstream-1
git add lean4_formal_proofs/lakefile.lean lean4_formal_proofs/neuro_symbolic.lean lean4_formal_proofs/neuro_symbolic/ lean4_formal_proofs/.github/
git commit -m "feat: setup S20 recurrence formal proof workspace"
git checkout main
git merge feature/workstream-1
git push origin main
curl -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter/releases \
  -d '{"tag_name":"v0.2.0","target_commitish":"main","name":"Release v0.2.0: S20 Recurrence","body":"Initial formal proof structures for S20 recurrence."}'
