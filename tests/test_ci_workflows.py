import json
from pathlib import Path

WORKFLOWS_DIR = Path('.github/workflows')
SETUP_ACTION = Path('.github/actions/setup-env/action.yml')


def _step_uses_before_local_action(workflow_text: str) -> list[str]:
    previous_uses = ''
    violations = []
    for line in workflow_text.splitlines():
        stripped = line.strip()
        if stripped.startswith('- uses:'):
            uses = stripped.removeprefix('- uses:').strip()
            if uses.startswith('./') and previous_uses != 'actions/checkout@v4':
                violations.append(uses)
            previous_uses = uses
    return violations


def test_workflows_checkout_repository_before_local_actions():
    violations = {}
    for workflow in WORKFLOWS_DIR.glob('*.yml'):
        local_action_violations = _step_uses_before_local_action(workflow.read_text())
        if local_action_violations:
            violations[str(workflow)] = local_action_violations

    assert not violations, violations


def test_setup_action_keeps_checkout_responsibility_in_workflows():
    action_text = SETUP_ACTION.read_text()

    assert 'actions/checkout' not in action_text
    assert 'uv sync --frozen' in action_text
    assert 'actions/setup-python@v5' in action_text
    assert 'ansible-galaxy collection install' in action_text
    assert 'ansible-lint' in action_text
    assert 'docker requests' in action_text


def test_setup_action_does_not_scan_empty_known_hosts_input():
    action_text = SETUP_ACTION.read_text()

    assert 'ssh-keyscan -H "${{ inputs.ssh-known-hosts }}"' not in action_text
    assert 'if [ -n "${{ inputs.ssh-known-hosts }}" ]; then' in action_text
    assert 'inputs.ssh-private-key-b64' in action_text
    assert 'base64 --decode > ~/.ssh/id_rsa' in action_text


def test_ansible_requirements_install_docker_collection():
    requirements_text = Path('ansible/requirements.yml').read_text()

    assert 'community.docker' in requirements_text


def test_pull_request_workflow_runs_tests_and_publishes_junit_results():
    workflow_text = (WORKFLOWS_DIR / 'test.yml').read_text()

    assert 'pull_request:' in workflow_text
    assert 'branches: [main]' in workflow_text
    assert "install-ansible: 'true'" in workflow_text
    assert 'uv run ansible-lint ansible' in workflow_text
    assert 'uv run pytest --junitxml=test-results.xml -v' in workflow_text
    assert 'EnricoMi/publish-unit-test-result-action@v2' in workflow_text
    assert 'files: test-results.xml' in workflow_text


# def test_deploy_workflow_gates_release_and_deploy_on_tests_and_release():
#     workflow_text = (WORKFLOWS_DIR / 'deploy.yml').read_text()
#
#     assert 'push:' in workflow_text
#     assert 'branches: [main, dev]' in workflow_text
#     assert 'release:' in workflow_text
#     assert 'needs: test' in workflow_text
#     assert 'fetch-depth: 0' in workflow_text
#     assert 'new_release_git_tag' in workflow_text
#     assert 'GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}' in workflow_text
#     assert 'DOCKER_IMAGE_NAME: ${{ secrets.DOCKER_IMAGE_NAME }}' in workflow_text
#     assert (
#         'DOCKER_IMAGE_TAG: ${{ needs.release.outputs.new_release_git_tag }}'
#         in workflow_text
#     )
#     assert 'DOCKER_USER: ${{ secrets.DOCKER_USER }}' in workflow_text
#     assert 'DOCKER_TOKEN: ${{ secrets.DOCKER_TOKEN }}' in workflow_text
#     assert 'ENV: ${{ secrets.ENV }}' in workflow_text
#     assert 'VM_HOST: ${{ secrets.VM_HOST }}' in workflow_text
#     assert 'VM_USER: ${{ secrets.VM_USER }}' in workflow_text
#     assert 'ssh-private-key-b64: ${{ secrets.SSH_PRIVATE_KEY_B64 }}' in workflow_text
#     assert 'ssh-known-hosts: ${{ secrets.SSH_KNOWN_HOSTS }}' in workflow_text
#     assert 'build-and-deploy:' in workflow_text
#     assert 'needs: release' in workflow_text
#     assert "needs.release.outputs.new_release_published == 'true'" in workflow_text
#     assert 'uv run ansible-playbook ansible/playbooks/build-image.yml' in workflow_text
#     assert 'uv run ansible-playbook ansible/playbooks/deploy.yml' in workflow_text


def test_vm_initialization_is_manual_and_default_branch_only():
    workflow_text = (WORKFLOWS_DIR / 'init-vm.yml').read_text()

    assert 'workflow_dispatch:' in workflow_text
    assert (
        "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        in workflow_text
    )
    assert 'VM_HOST: ${{ secrets.VM_HOST }}' in workflow_text
    assert 'VM_USER: ${{ secrets.VM_USER }}' in workflow_text
    assert 'ssh-private-key-b64: ${{ secrets.SSH_PRIVATE_KEY_B64 }}' in workflow_text
    assert 'ssh-known-hosts: ${{ secrets.SSH_KNOWN_HOSTS }}' in workflow_text
    assert 'uv run ansible-playbook ansible/playbooks/init-vm.yml' in workflow_text


# def test_semantic_release_config_supports_python_backend_without_npm():
#     release_config_path = Path('release.config.cjs')
#     release_config_bytes = release_config_path.read_bytes()
#     release_config_text = release_config_bytes.decode('utf-8')
#
#     assert not release_config_bytes.startswith(b'\xef\xbb\xbf')
#     assert not Path('.releaserc.json').exists()
#     assert 'module.exports = {' in release_config_text
#     assert "'main'" in release_config_text
#     assert "name: 'dev'" in release_config_text
#     assert 'prerelease: true' in release_config_text
#     assert '@semantic-release/commit-analyzer' in release_config_text
#     assert '@semantic-release/release-notes-generator' in release_config_text
#     assert '@semantic-release/github' in release_config_text
#     assert '@semantic-release/npm' not in release_config_text
#
#
# def test_build_image_playbook_uses_current_ansible_python():
#     playbook_text = Path('ansible/playbooks/build-image.yml').read_text()
#
#     assert (
#         'ansible_python_interpreter: "{{ ansible_playbook_python }}"'
#         in playbook_text
#     )
