import xml.etree.ElementTree as ET

# Load the Ahmedabad OSM file
file_path = "ahmedabad.osm"
tree = ET.parse(file_path)
root = tree.getroot()

# Extract ways (roads and their node connections)
ways = {}
for way in root.findall("way"):
    way_id = way.get("id")
    node_refs = [nd.get("ref") for nd in way.findall("nd")]
    ways[way_id] = node_refs

# Create adjacency list
adj_list = {}

for way_id, node_refs in ways.items():
    for i in range(len(node_refs) - 1):
        node1 = node_refs[i]
        node2 = node_refs[i + 1]

        if node1 not in adj_list:
            adj_list[node1] = []
        if node2 not in adj_list:
            adj_list[node2] = []

        adj_list[node1].append(int(node2))
        adj_list[node2].append(int(node1))

print(f"✅ Adjacency list created with {len(adj_list)} nodes")

with open("adjacency_list.txt", "w") as file:
    for vertice in adj_list:
        file.write(f"{vertice} " + " ".join(map(str, adj_list[vertice])) + "\n")
print(f"✅ Adjacency list saved as {file.name}")

        