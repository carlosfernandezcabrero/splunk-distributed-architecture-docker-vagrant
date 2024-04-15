import { $ } from "bun";

interface MachineCommand {
    vagrantMachineName: string[];
    dockerContainerName: string;
    expectedDockerFrom: string;
}

const EXPECTED_DOCKER_FROM = "CentOS Linux 7 (Core)";

export const machinesCommandsCore: MachineCommand[] = [
    {
        vagrantMachineName: ["sh1", "sh2", "test_sh"],
        dockerContainerName: "splunk-sh",
        expectedDockerFrom: EXPECTED_DOCKER_FROM,
    },
    {
        vagrantMachineName: ["idx1", "idx2", "test_idx"],
        dockerContainerName: "splunk-idx",
        expectedDockerFrom: EXPECTED_DOCKER_FROM,
    },
    {
        vagrantMachineName: ["manager"],
        dockerContainerName: "splunk-manager",
        expectedDockerFrom: EXPECTED_DOCKER_FROM,
    },
    {
        vagrantMachineName: ["hf"],
        dockerContainerName: "splunk-hf",
        expectedDockerFrom: EXPECTED_DOCKER_FROM,
    },
];
export const machinesCommandsUf: MachineCommand[] = [
    {
        vagrantMachineName: ["uf1"],
        dockerContainerName: "uf",
        expectedDockerFrom: EXPECTED_DOCKER_FROM,
    },
];

export function checkDockerFrom(machineCommands: MachineCommand[]) {
    machineCommands.forEach(({ vagrantMachineName, dockerContainerName }) => {
        vagrantMachineName.forEach(async (vagrantMachineName) => {
            const os =
                await $`vagrant ssh ${vagrantMachineName} -c 'docker exec -it ${dockerContainerName} bash -c "grep PRETTY_NAME /etc/os-release"'`.text();
            console.log(`${vagrantMachineName}: ${os}\n`.trim());
        });
    });
}
