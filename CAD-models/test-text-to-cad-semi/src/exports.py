"""Export standing deliverables (STEP, GLB, STL, 3MF) for the Tesla Semi truck."""

from cad import model
from truck import tesla_semi_truck


def export_deliverables():
    truck_doc = tesla_semi_truck()
    truck_doc.export(
        "STEP/tesla_semi.step",
        "GLB/tesla_semi.glb",
        "STL/tesla_semi.stl",
        "3MF/tesla_semi.3mf",
    )
    print("Exported all deliverables.")


if __name__ == "__main__":
    export_deliverables()
