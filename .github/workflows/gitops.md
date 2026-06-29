  update-gitops:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - name: Checkout GitOps repository
        uses: actions/checkout@v4
        with:
          repository: ${{ secrets.GITOPS_REPO }}
          token: ${{ secrets.GITOPS_TOKEN }}
          path: gitops

      - name: Setup Kustomize
        uses: imranismail/setup-kustomize@v2

      - name: Update image tag in kustomization
        run: |
          cd gitops/k8s
          kustomize edit set image \
            ${{ secrets.DOCKERHUB_USERNAME }}/registro-atividades-backend=\
            ${{ secrets.DOCKERHUB_USERNAME }}/registro-atividades-backend:${{ needs.build-and-push.outputs.image_tag }}

      - name: Commit and push
        run: |
          cd gitops
          git config user.name "github-actions"
          git config user.email "github-actions@users.noreply.github.com"
          git add .
          git commit -m "chore: update backend image tag to ${{ needs.build-and-push.outputs.image_tag }}" || echo "No changes to commit"
          git push